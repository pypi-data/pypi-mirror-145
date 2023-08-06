import asyncio
import logging
from typing import List

from aiohttp import web
from aiohttp.web_runner import TCPSite, AppRunner

from cenao.app import AppFeature
from cenao.view import View


class WebAppFeature(AppFeature):
    NAME = 'web'

    views: List[View] = []
    host: str
    port: int

    aiohttp_app: web.Application
    runner: AppRunner

    def on_init(self):
        self.host = self.config.get('host', '0.0.0.0')
        self.port = int(self.config.get('port', 8000))

        app = web.Application(
            loop=self.app.loop
        )
        routes_len = 0
        for ft in self.app.ft:
            for view in ft.VIEWS:
                view.init(ft)
                app.router.add_view(view.ROUTE, view)
                routes_len += 1
        self.logger.info('Registered %d routes', routes_len)

        self.runner = AppRunner(app, logger=self.logger)

    async def on_startup(self):
        self.logger.info('Starting on %s:%d', self.host, self.port)
        await self.runner.setup()
        site = TCPSite(
            self.runner,
            self.host,
            self.port,
        )
        await site.start()
        while True:
            await asyncio.sleep(3600)

    async def on_shutdown(self):
        self.logger.info('Stopping webserver')
        await self.runner.cleanup()
