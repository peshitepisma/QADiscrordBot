import os
import discord
from discord_slash import SlashCommand, utils
from db import Database
from asyncio import sleep
from misc import get_full_path
from discord.ext import commands
from misc.addition import Server


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database()
        self.db.create()
        self.__slash = SlashCommand(self, sync_on_cog_reload=True, sync_commands=True, debug_guild=Server.id)
        self.__load_cogs()
        self.remove_command('help')

    async def on_ready(self):
        print('Logged on as', self.user)
        while self.user:
            await self.change_presence(status=discord.Status.online, activity=discord.Game("тестирую твой код"))
            await sleep(5)
            await self.change_presence(status=discord.Status.online, activity=discord.Game("/help"))

    async def on_member_join(self, member):
        role = member.guild.get_role(role_id=911196795210694687)
        await member.add_roles(role)

    async def __delete_commands(self):
        await utils.manage_commands.remove_all_commands_in(911197595429371924, os.environ.get('TOKEN', ''),
                                                           guild_id=Server.id)

    def __load_cogs(self):
        excluded_cogs = ['base.py', '__init__.py']
        for i, filename in enumerate(os.listdir(get_full_path('cogs'))):
            if filename.endswith('.py') and filename not in excluded_cogs:
                self.load_extension(f"cogs.{filename[:-3]}")
        print('All Cogs installed')
