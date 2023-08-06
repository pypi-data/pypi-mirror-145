import logging
from typing import TYPE_CHECKING, Dict, Union, Generator, Any

from aiohttp import abc, hdrs, web
from aiohttp.web_exceptions import HTTPMethodNotAllowed

if TYPE_CHECKING:
    from cenao.app import Application, AppFeature


class View(abc.AbstractView):
    ROUTE: str

    logger: logging.Logger
    ft: 'AppFeature'

    aiohttp_view: web.View

    @property
    def app(self) -> 'Application':
        return self.ft.app

    @classmethod
    def init(cls, ft: 'AppFeature'):
        cls.ft = ft
        cls.logger = logging.getLogger(cls.__name__)

    @property
    def remote_ip(self) -> str:
        if xff := self.request.headers.get('X-FORWARDED-FOR', ''):
            return xff
        if xri := self.request.headers.get('X-REAL-IP', ''):
            return xri
        return self.request.remote

    async def _iter(self) -> web.StreamResponse:
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()

        try:
            resp = await method()
        except Exception as e:
            e_msg = 'Got exception while handling request'
            self.logger.exception(e_msg, exc_info=e)
            return web.json_response({'ok': False, 'message': e_msg}, status=500)
        if resp is None:
            return web.json_response({'ok': True})

        if isinstance(resp, dict):
            return web.json_response(resp)

        return resp

    def __await__(self) -> Generator[Any, None, abc.StreamResponse]:
        return self._iter().__await__()

    def _raise_allowed_methods(self) -> None:
        allowed_methods = {m for m in hdrs.METH_ALL if hasattr(self, m.lower())}
        raise HTTPMethodNotAllowed(self.request.method, allowed_methods)

    async def get(self) -> Union[Dict, None, web.Response]:
        pass

    async def post(self) -> Union[Dict, None, web.Response]:
        pass

    async def put(self) -> Union[Dict, None, web.Response]:
        pass

    async def delete(self) -> Union[Dict, None, web.Response]:
        pass
