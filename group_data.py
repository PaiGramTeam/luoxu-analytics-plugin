from typing import List, Dict, Optional

import asyncpg

from cashews import cache
from telethon import TelegramClient
from telethon.errors import StatsMigrateError
from telethon.tl.functions.stats import GetMegagroupStatsRequest
from telethon.utils import get_input_channel
from telethon.tl.types.stats import MegagroupStats

cache.setup("mem://")


@cache(ttl="1h", key="{cid}")
async def get_group_data(cid: int, client: TelegramClient, db) -> List[Dict]:
    group = get_input_channel(await client.get_input_entity(cid))
    try:
        result: MegagroupStats = await client(GetMegagroupStatsRequest(
            channel=group,
            dark=True
        ))
    except StatsMigrateError as e:
        sender = await client._borrow_exported_sender(e.dc)
        result: MegagroupStats = await client._call(sender, GetMegagroupStatsRequest(
            channel=group,
            dark=True
        ))
    data = [i.to_dict() for i in result.top_posters]
    for i in data:
        i['name'] = await get_user_name(db, i['user_id'])
    return data


async def get_user_name(db, uid: int) -> str:
    async with db.get_conn() as conn:
        conn: "asyncpg.pool.connection.Connection"
        sql = f"""\
        SELECT name
        FROM usernames 
        WHERE {uid} = ANY ( uid ) 
        ORDER BY last_seen DESC 
        LIMIT 1;"""
        value = await conn.fetchval(sql)
        if value:
            return value
        return "Unknown"
