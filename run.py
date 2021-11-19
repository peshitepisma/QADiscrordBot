import os

import discord

from bot import Bot


def main():
    bot = Bot(command_prefix='!', intents=discord.Intents.all())
    bot.run(os.environ.get('TOKEN', ''))


if __name__ == "__main__":
    main()
