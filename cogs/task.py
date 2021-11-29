from discord.ext import commands
from discord.ext.commands import Context
from discord_slash.utils.manage_commands import create_option
from cogs import Base
from sqlalchemy import exc
from discord_slash import cog_ext, SlashContext
from cogs.base import parse_channel
from misc.addition import Server


class Task(Base):
    channel_name = 'config'

    @cog_ext.cog_slash(description='Получить список доступных заданий')
    async def tasks(self, ctx: SlashContext):
        result_str = ''
        for i, task in enumerate(self.db.get_tasks()):
            result_str += f'{i + 1}. {task.name}\n'
        if not result_str:
            await ctx.send('Список заданий пуст', hidden=True)
        else:
            await ctx.send(f'Доступные задания:```\n{result_str}```', hidden=True)

    @commands.command()
    @parse_channel(channel_name)
    async def add_task(self, ctx: Context, task_name, *, description):
        try:
            description = description.strip('```')
            self.db.create_task(task_name, description)
            await ctx.send(f'Добавлено задание: {task_name}')
        except exc.IntegrityError:
            self.db.session.rollback()
            await ctx.send(f'Задание с таким именем уже существует: {task_name}')

    @commands.command()
    @parse_channel(channel_name)
    async def add_test(self, ctx: Context, task_name, *, test):
        task = self.db.get_task_by_name(task_name)
        if task:
            tests = test.replace('```', '').strip().split('**')
            tests = [line.strip().split('*') for line in tests]
            for test in tests:
                self.db.add_test_for_task(task, *test)
            await ctx.send(f'Добавлен тесткейс в задание: {task_name}')
        else:
            await ctx.send(f'Задание с таким именем не существует: {task_name}')

    @cog_ext.cog_slash(description='Удалить определенное задание', options=[
        create_option(name="task_name", description="Имя существующего задания", option_type=3, required=True)],
                       permissions=Server.get_cmd_permissions())
    async def remove_task(self, ctx: SlashContext, task_name):
        task = self.db.get_task_by_name(task_name)
        if task:
            self.db.delete_task(task)
            await ctx.send(f'Удалено задание: {task_name}', hidden=True)
        else:
            await ctx.send(f'Задания не сусществует: {task_name}', hidden=True)

    @cog_ext.cog_slash(description='Посмотреть определенное задание', options=[
        create_option(name="task_name", description="Имя существующего задания", option_type=3, required=True)])
    async def read_task(self, ctx: SlashContext, task_name):
        task = self.db.get_task_by_name(task_name)
        if task:
            await ctx.send(f'{task.name}\n```{task.description}```', hidden=True)
        else:
            await ctx.send(f'Задания не сусществует: {task_name}', hidden=True)

    @cog_ext.cog_slash(description='Удалить все задания', permissions=Server.get_cmd_permissions())
    async def clear_tasks(self, ctx: SlashContext):
        self.db.delete_all_tasks()
        await ctx.send(f'Список заданий очищен', hidden=True)


def setup(bot):
    bot.add_cog(Task(bot))
