import os
import sys
import time
from commands import Base
from misc import get_full_path
from subprocess import Popen, PIPE
from prettytable import PrettyTable


class Test(Base):

    async def run(self):
        await self.message.delete()
        if self.message.content.startswith('!test'):
            text = self.message.content.strip().split('\n')
            task = self.db.get_task_by_name(self.get_task_name(text[0], '!test'))
            if not task:
                await self.message.author.send('```\nТакого задания не существует```')
                return
            if not task.tests:
                await self.message.author.send('```\nТесты для этого задания еще не добавлены```')
                return
            code = '\n'.join(text[1:])
            if not code:
                await self.message.author.send('```\nНе указан код программмы```')
                return
            file_name = get_full_path(f'task.py')
            with open(file_name, 'w', encoding='utf-8') as f:
                for line in code:
                    f.write(line)
            table = PrettyTable()
            table.field_names = ["Test №", "Status", "Time"]
            for i, test in enumerate(task.tests):
                start_time = time.monotonic()
                out, error = self.compare_console_output(file_name, test)
                if error:
                    await self.message.author.send(f'```\n{error}```')
                    table.clear_rows()
                    break
                if out:
                    table.add_row([f'{i + 1}', "✅", f'{round(time.monotonic()-start_time, 3)} sec'])
                else:
                    table.add_row([f"{i + 1}", "❌", f'-'])
            os.remove(file_name)
            if table.rows:
                await self.message.author.send(f'```\n{table}```')

    def compare_console_output(self, file_name, test):
        p = Popen([sys.executable, file_name], stdout=PIPE, stdin=PIPE, stderr=PIPE, encoding='utf-8')
        out, error = p.communicate(input='\n'.join(test.input.strip().split()))
        if not error:
            return out.split() == test.output.strip().split(), None
        else:
            return None, error
