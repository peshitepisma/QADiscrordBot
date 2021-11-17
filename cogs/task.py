from discord.ext import commands
from sqlalchemy import exc
from cogs import Base
from cogs.base import parse_channel


class Task(Base):
    channel_name = 'config'

    @commands.command()
    @parse_channel(channel_name)
    async def task_list(self, ctx):
        result_str = ''
        for i, task in enumerate(self.db.get_tasks()):
            result_str += f'{i + 1}. {task.name}\n'
        if not result_str:
            await ctx.author.send(f'Список заданий пуст')
        else:
            await ctx.author.send(f'Доступные задания:```\n{result_str}```')

    @commands.command()
    @parse_channel(channel_name)
    async def add_task(self, ctx, task_name):
        try:
            self.db.create_task(task_name)
            await ctx.channel.send(f'Добавлено задание: {task_name}')
        except exc.IntegrityError:
            self.db.session.rollback()
            await ctx.channel.send(f'Задание с таким именем уже существует: {task_name}')

    @commands.command()
    @parse_channel(channel_name)
    async def add_test(self, ctx, task_name, *, test):
        task = self.db.get_task_by_name(task_name)
        tests = test.strip().replace('```', '').strip()
        tests = tests.split('**')
        tests = [line.strip().split('*') for line in tests]
        if task:
            for test in tests:
                self.db.add_test_for_task(task, *test)
            await ctx.channel.send(f'Добавлен тесткейс в задание: {task_name}')
        else:
            await ctx.channel.send(f'Задание с таким именем не существует: {task_name}')

    @commands.command()
    @parse_channel(channel_name)
    async def remove_task(self, ctx, task_name):
        task = self.db.get_task_by_name(task_name)
        if task:
            self.db.delete_task(task)
            await ctx.channel.send(f'Удалено задание: {task_name}')
        else:
            await ctx.channel.send(f'Задания не сусществует: {task_name}')

    @commands.command()
    @parse_channel(channel_name)
    async def clear(self, ctx):
        self.db.delete_all_tasks()
        await ctx.channel.send(f'Список заданий очищен')


def setup(bot):
    bot.add_cog(Task(bot))
