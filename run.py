import os
from bot import Bot


def main():
    bot = Bot(command_prefix='!')
    bot.run(os.environ.get('TOKEN', ''))


if __name__ == "__main__":
    main()
