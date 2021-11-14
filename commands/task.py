import discord
from sqlalchemy import exc
from commands import Base
from prettytable import PrettyTable


class Task(Base):

    def __init__(self, bot, message: discord.Message):
        super().__init__(bot, message)
        self.commands = {
            '!add_task': self.add_task,
            '!add_test': self.add_test,
            '!remove_task': self.remove_task,
            '!task_list': self.task_list,
            '!clear': self.clear,
        }

    async def task_list(self):
        result_str = ''
        for i, task in enumerate(self.db.get_tasks()):
            result_str += f'{i+1}. {task.name}\n'
        if not result_str:
            await self.message.author.send(f'Список заданий пуст')
        else:
            await self.message.author.send(f'Доступные задания:```\n{result_str}```')

    async def add_task(self):
        task_name = self.get_task_name(self.message.content, '!add_task')
        try:
            self.db.create_task(task_name)
            await self.message.channel.send(f'Добавлено задание: {task_name}')
        except exc.IntegrityError:
            self.db.session.rollback()
            await self.message.channel.send(f'Задание с таким именем уже существует: {task_name}')

    async def add_test(self):
        msg = self.message.content.strip().split('\n')
        task_name = self.get_task_name(msg[0], '!add_test')
        task = self.db.get_task_by_name(task_name)
        if task:
            self.db.add_test_for_task(task, input=msg[1], output=msg[2])
            await self.message.channel.send(f'Добавлен тесткейс в задание: {task_name}')
        else:
            await self.message.channel.send(f'Задание с таким именем не существует: {task_name}')

    async def remove_task(self):
        task_name = self.get_task_name(self.message.content, '!remove_task')
        task = self.db.get_task_by_name(task_name)
        if task:
            self.db.delete_task(task)
            await self.message.channel.send(f'Удалено задание: {task_name}')
        else:
            await self.message.channel.send(f'Задания не сусществует: {task_name}')

    async def clear(self):
        self.db.delete_all_tasks()
        await self.message.channel.send(f'Список заданий очищен')

    async def run(self):
        for key in self.commands.keys():
            if self.message.content.startswith(key):
                await self.commands[key]()
                break
