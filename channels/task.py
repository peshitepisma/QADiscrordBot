import discord

from channels import Base


class Task(Base):

    def __init__(self, bot, message: discord.Message):
        super().__init__(bot, message)
        self.commands = {
            '!add_task': self.add_task,
            '!add_test': self.add_test,
            '!remove_task': self.remove_task,
            '!clear': self.clear,
        }

    async def add_task(self):
        task_name = self.get_task_name(self.message.content, '!add_task')
        self.bot.db.create_task(task_name)
        await self.message.channel.send(f'Добавлено задание: {task_name}')

    async def add_test(self):
        msg = self.message.content.strip().split('\n')
        task_name = self.get_task_name(msg[0], '!add_test')
        self.bot.db.add_test_for_task(task_name=task_name, input=msg[1], output=msg[2])
        await self.message.channel.send(f'Добавлен тесткейс в задание: {task_name}')

    async def remove_task(self):
        task_name = self.get_task_name(self.message.content, '!remove_task')
        self.bot.db.delete_task(task_name)
        await self.message.channel.send(f'Удалено задание: {task_name}')

    async def clear(self):
        self.bot.db.delete_all_tasks()
        await self.message.channel.send(f'Список заданий очищен')

    async def run(self):
        for key in self.commands.keys():
            if self.message.content.startswith(key):
                await self.commands[key]()
                break
