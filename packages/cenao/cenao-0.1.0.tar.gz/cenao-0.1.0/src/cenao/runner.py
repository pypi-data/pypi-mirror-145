import argparse
import logging

from cenao.app import Application
from cenao.config import Config


class ApplicationRunner:
    app: Application

    def __init__(self, app: Application):
        self.app = app

    def run(self):
        parser = argparse.ArgumentParser(description='Run a cenao application')
        parser.add_argument('-c', '--config', help='Application configuration', default=None)
        parser.add_argument(
            '-e', '--env-prefix',
            help='Prefix of environment variables which would redefine config values',
            default='APP',
        )
        args = parser.parse_args()

        config = Config(args.config)
        config.process_env(args.env_prefix)

        self._init_logger(config)
        self.app.init(config)
        self.app.run()

    def _init_logger(self, config):
        config = config.get('logging', {})
        fmt = config.get('format', '%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
        level = config.get('level', 'INFO')
        file = config.get('file', f'{self.app.NAME.lower()}.log')
        stdout = config.get('stdout', True)

        logging.basicConfig(
            level=level,
            filename=file,
            format=fmt
        )

        if stdout:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter(fmt)
            handler.setFormatter(formatter)

            logger = logging.getLogger('')
            logger.addHandler(handler)
