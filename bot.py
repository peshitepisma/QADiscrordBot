import os
from misc import get_full_path
from discord.ext import commands
from db import Database


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database()
        self.db.create()

    async def on_ready(self):
        print('Logged on as', self.user)
        self.load_cogs()

    def load_cogs(self):
        for filename in os.listdir(get_full_path('cogs')):
            if filename.endswith('.py') and filename not in ['base.py', '__init__.py']:
                self.load_extension(f"cogs.{filename[:-3]}")
