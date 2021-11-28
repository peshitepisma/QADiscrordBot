import os
import sys
import time
from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import SlashContext
from cogs import Base
from cogs.base import parse_channel
from misc import get_full_path
from subprocess import Popen, PIPE
from prettytable import PrettyTable


class Test(Base):
    channel_name = 'tester'
    file_name = get_full_path(f'task.py')

    @commands.command()
    @parse_channel(channel_name)
    async def test(self, ctx: Context, task_name, *, code):
        task = self.db.get_task_by_name(task_name)
        await ctx.message.delete()
        if not task:
            await ctx.author.send('```\nТакого задания не существует```')
            return
        if not task.tests:
            await ctx.author.send('```\nТесты для этого задания еще не добавлены```')
            return
        code = code.strip().replace('```', '').replace('py\n', '')
        if not code:
            await ctx.author.send('```\nНе указан код программмы```')
            return

        self.create_py_file(code)
        answer_table: PrettyTable = await self.test_py_file(ctx, task)
        os.remove(self.file_name)
        if answer_table.rows:
            await ctx.author.send(f'Задание: {task.name}\n```{answer_table}```')

    async def test_py_file(self, ctx: Context, task) -> PrettyTable:
        table = PrettyTable()
        table.field_names = ["Test №", "Status", "Time"]
        for i, test in enumerate(task.tests):
            start_time = time.monotonic()
            out, error = self.compare_console_output(test)
            if error:
                await ctx.send(f'```py\n{error}```')
                table.clear_rows()
                return table
            elif out:
                table.add_row([f'{i + 1}', "✅", f'{round(time.monotonic() - start_time, 3)} sec'])
            else:
                table.add_row([f"{i + 1}", "❌", f'-'])
        return table

    def create_py_file(self, code) -> None:
        with open(self.file_name, 'w', encoding='utf-8') as f:
            for line in code:
                f.write(line)

    def compare_console_output(self, test):
        p = Popen([sys.executable, self.file_name], stdout=PIPE, stdin=PIPE, stderr=PIPE, encoding='utf-8')
        out, error = p.communicate(input='\n'.join(test.input.split('\n')))
        if not error:
            return out.split() == test.output.split(), None
        else:
            return None, error


def setup(bot):
    bot.add_cog(Test(bot))
