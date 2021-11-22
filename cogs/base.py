import functools
from db import Database
from typing import Union
from discord.ext import commands
from discord.ext.commands.context import Context


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

