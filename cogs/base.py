import functools
from typing import Union

from discord.ext.commands import Context

from db import Database
from discord.ext import commands


class Base(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.db: Database = bot.db


def parse_channel(channel_name: Union[str, list]):
    if isinstance(channel_name, str):
        channel_name = [channel_name]
    channel_name = [i.lower() for i in channel_name]

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ctx: Context, *args, **kwargs):
            if ctx.channel.name.lower() in channel_name:
                await func(self, ctx, *args, **kwargs)

        return wrapper

    return decorator
