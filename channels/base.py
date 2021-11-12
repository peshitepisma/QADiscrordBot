import discord


class Base:
    def __init__(self, bot, message: discord.Message):
        self.bot = bot
        self.message = message

    async def run(self):
        raise NotImplementedError
