import logging

from aiohttp import web
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError

from .group_data import get_group_data

logger = logging.getLogger('luoxu_plugins.analytics')


class GroupAnalyticsHandler:
    def __init__(self, client, db):
        self.client = client
        self.db = db

    async def get(self, request: web.Request):
        if cid_str := request.query.get('cid'):
            try:
                uid = int(cid_str)
                await self.client.get_entity(uid)
            except (ValueError, ChannelPrivateError):
                raise web.HTTPForbidden(headers={
                    'Cache-Control': 'public, max-age=86400',
                })
            return web.json_response(await get_group_data(uid, self.client, self.db))
        else:
            raise web.HTTPNotFound


async def register(indexer, client: TelegramClient):
    port: int = int(indexer.config['plugin']['analytics']['port'])

    handler = GroupAnalyticsHandler(client, indexer.dbstore)

    app = web.Application()
    app.router.add_get('/api/group_analytics', handler.get)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner,
        indexer.config['web']['listen_host'], port,
    )
    await site.start()
