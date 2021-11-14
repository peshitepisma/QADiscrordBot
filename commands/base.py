import discord
from db import Database


class Base:
    def __init__(self, bot, message: discord.Message):
        self.bot = bot
        self.db: Database = bot.db
        self.message = message

    @staticmethod
    def get_task_name(msg: str, parse: str):
        return msg.replace(parse, "").strip().lower().capitalize()

    async def run(self):
        raise NotImplementedError
