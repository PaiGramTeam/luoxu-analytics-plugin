from typing import List, Dict

from cashews import cache
from telethon import TelegramClient
from telethon.tl.functions.stats import GetMegagroupStatsRequest
from telethon.utils import get_input_channel
from telethon.tl.types.stats import MegagroupStats

cache.setup("mem://")


@cache(ttl="1h", key="{cid}")
async def get_group_data(cid: int, client: TelegramClient) -> List[Dict]:
    group = get_input_channel(await client.get_input_entity(cid))
    result: MegagroupStats = await client(GetMegagroupStatsRequest(
        channel=group,
        dark=True
    ))
    return [i.to_dict() for i in result.top_posters]
