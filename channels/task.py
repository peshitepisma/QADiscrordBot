import os

from channels import Base
from settings import PathManager


class Task(Base):

    async def run(self):
        if self.message.content.startswith('!add_task'):
            self.bot.tasks.append([])
            fl = open(PathManager.get_full_path(f'task/{len(self.bot.tasks) - 1}.txt'), 'w')
            fl.close()
            await self.message.channel.send(f'Добавлено задание номер {len(self.bot.tasks) - 1}')

        if self.message.content.startswith('!add_test'):
            msg = self.message.content.split()
            task_num = int(msg[1])

            msg = self.message.content.split('\n')
            input = msg[1]
            output = msg[2]

            fl = open(PathManager.get_full_path(f'task/{task_num}.txt'), 'a')
            fl.write(f'{input}\n')
            fl.write(f'{output}\n')
            fl.close()

            self.bot.tasks[task_num].append({'input': input, 'output': output})
            await self.message.channel.send(f'Добавлен тесткейс в задание номер {task_num}')

        if self.message.content.startswith('!remove_test'):
            msg = self.message.content.split()
            task_num = int(msg[1])
            test_num = int(msg[2])

            del self.bot.tasks[task_num][test_num]

            fl = open(PathManager.get_full_path(f'task/{msg[1]}.txt'), 'r')
            data = fl.readlines()
            fl.close()

            fl = open(PathManager.get_full_path(f'task/{msg[1]}.txt'), 'w')
            for i in range(len(data)):
                if any((i == test_num, i == test_num + 1)):
                    continue
                fl.write(data[i])
            fl.close()

            await self.message.channel.send(f'Удален тесткейс в задании номер {task_num}')

        if self.message.content.startswith('!clear_tests'):
            msg = self.message.content.split()
            self.bot.tasks[int(msg[1])].clear()
            fl = open(PathManager.get_full_path(f'task/{msg[1]}.txt'), 'w')
            fl.close()
            await self.message.channel.send(f'Удалены все тесткейсы задания номер {msg[1]}')

        elif self.message.content.startswith('!clear'):
            self.bot.tasks.clear()
            for fl in os.listdir('task'):
                os.remove(PathManager.get_full_path(f'task/{fl}'))
            await self.message.channel.send(f'Список заданий очищен')
