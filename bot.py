import discord
from commands import Task, Test
from db import Database


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database()
        self.db.create()
        self.channels = {
            'test_bot_mgmt': Task,
            'test_bot_channel': Test,
        }

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.channel.name in self.channels.keys():
            await self.channels[message.channel.name](bot=self, message=message).run()