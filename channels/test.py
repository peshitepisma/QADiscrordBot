import os
import sys
import time
from subprocess import Popen, PIPE
from channels import Base
from misc import get_full_path


class Test(Base):

    async def run(self):
        if self.message.content.startswith('!test'):
            result_string = ''
            await self.message.delete()
            text = self.message.content.strip().split('\n')
            task = self.bot.db.get_task_by_name(self.get_task_name(text[0], '!test'))
            code = '\n'.join(text[1:])
            if code:
                await self.message.channel.send("Тестирую. Попей чаю 🍵")
                with open(get_full_path(f'task.py'), 'w', encoding='utf-8') as f:
                    for line in code:
                        f.write(line)
                for i, test in enumerate(task.tests):
                    start_time = time.monotonic()
                    if self.compare_console_output(test):
                        result_string += f'✅ Тест {i + 1} - успешно ({round(time.monotonic()-start_time, 3)} sec)\n'
                    else:
                        result_string += f'❌ Тест {i + 1} - неверный ответ\n'
                os.remove(get_full_path("task.py"))
                await self.message.channel.send(f'```\n{result_string}```')

    def compare_console_output(self, test) -> bool:
        p = Popen([sys.executable, get_full_path(f'task.py')], stdout=PIPE, stdin=PIPE, stderr=PIPE, encoding='utf-8')
        out, err = p.communicate(input='\n'.join(test.input.strip().split()))
        return out.split() == test.output.strip().split()
