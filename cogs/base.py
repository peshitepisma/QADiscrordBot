import functools
from discord.ext import commands
from discord.ext.commands.context import Context
from db import Database


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: Database = bot.db


def parse_channel(channel_name: str = ''):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ctx: Context, *args, **kwargs):
            if ctx.channel.name.lower() == channel_name.lower():
                await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator

