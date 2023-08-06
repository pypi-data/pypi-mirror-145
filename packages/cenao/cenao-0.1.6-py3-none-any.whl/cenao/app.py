import asyncio
import logging
import signal
from abc import ABC
from typing import List, Optional, Type, Union

from cenao.config import Config
from cenao.exceptions import InvalidFeatureException
from cenao.view import View


class AppFeature(ABC):
    NAME: str
    CONF: Optional[str] = None
    VIEWS: List[View] = []

    app: 'Application'
    logger: logging.Logger

    def __init__(self, name: Optional[str] = None):
        if name:
            self.NAME = name.lower()

    def _get_config_group(self) -> str:
        if not self.CONF:
            return self.name
        else:
            return self.CONF.lower()

    @property
    def name(self):
        return self.NAME.lower()

    @property
    def config(self):
        return self.app.config.get(self._get_config_group(), {})

    def init(self, app: 'Application'):
        self.app = app
        self.logger = logging.getLogger(self.NAME)
        self.on_init()

    def on_init(self):
        pass

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass

    async def check_health(self) -> bool:
        return True


class Features(dict):
    def __init__(self):
        super().__init__()
        self.__dict__ = self

    def __iter__(self):
        return iter(self.values())


class Application(ABC):
    NAME: str
    FEATURES: List[Union[AppFeature, Type[AppFeature]]]

    config: Config
    logger: logging.Logger
    ft: Features = Features()
    loop: asyncio.AbstractEventLoop
    _task: Optional[asyncio.Task] = None

    def init_features(self):
        for feature in self.FEATURES:
            if isinstance(feature, AppFeature):
                self.logger.info('Init %s', feature.__class__.__name__)
                _feature = feature
            elif isinstance(feature(), AppFeature):
                self.logger.info('Init %s', feature.__name__)
                _feature = feature()
            else:
                raise InvalidFeatureException(feature)

            _feature.init(self)
            self.ft[_feature.name] = _feature

    def init(self, config):
        self.config = config
        self.logger = logging.getLogger(self.NAME + 'App')
        self.logger.info('Init application')
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, self.shutdown)
        self.loop.add_signal_handler(signal.SIGTERM, self.shutdown)

        self.on_init()
        self.init_features()

    def run(self):
        self.logger.info('Application started')
        features: List[AppFeature] = []
        ft: AppFeature
        for ft in self.ft:
            self.logger.info('Startup feature %s', ft.name)
            self._task = self.loop.create_task(ft.on_startup())
            try:
                self.loop.run_until_complete(self._task)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.exception('Got exception while feature startup: %r', e, exc_info=e)
                break
            features.append(ft)

        for ft in reversed(features):
            self.logger.info('Shutdown feature %s', ft.name)
            self._task = self.loop.create_task(ft.on_shutdown())
            try:
                self.loop.run_until_complete(self._task)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.exception('Got exception while feature shutdown: %r', e, exc_info=e)
                break

        self.logger.info('Application stopped')

    def shutdown(self):
        self.logger.info('Shutdown requested')
        if self._task:
            self._task.cancel()

    def on_init(self):
        pass
