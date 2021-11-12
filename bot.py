import os
import discord
import task
import time
import importlib
from settings import PathManager
from channels import Task, Test


def read_tasks() -> list[list[dict]]:
    tasks = []
    for file in os.listdir(PathManager.get_full_path('task')):
        tasks.append([])
        with open(PathManager.get_full_path(f'task/{file}'), 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                tasks[-1].append({
                    'input': lines[i].strip().split(),
                    'output': lines[i + 1].strip().split(),
                })
    return tasks


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.tasks = read_tasks()
        self.channels = {
            'test_bot_mgmt':  Task,
            'test_bot_channel': Test,
        }

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.channel.name in self.channels.keys():
            await self.channels[message.channel.name](bot=self, message=message).run()

    def transform_code(self, code, task_num):
        new_code = []
        for test_case_num in range(len(self.tasks[task_num])):
            new_code.append([])
            new_code[test_case_num] += ['class Func:\n', '    def func(self):\n', '        result____ = []\n']
            input_ctr = 0
            for i in range(len(code)):
                new_code[test_case_num].append('        ' + code[i] + '\n')
                if new_code[test_case_num][-1].find('print') != -1:
                    index = -1
                    for j in range(len(new_code[test_case_num][-1])):
                        if new_code[test_case_num][-1][j] == 'p':
                            index = j
                            break

                    new_code[test_case_num][-1] = new_code[test_case_num][-1][:index] + 'result____.append' + \
                                                  new_code[test_case_num][-1][index + 5:] + '\n'

                if new_code[test_case_num][-1].find('input(') != -1:
                    index = -1
                    for j in range(len(new_code[test_case_num][-1])):
                        if new_code[test_case_num][-1][j] == '=':
                            index = j

                    new_code[test_case_num][-1] = new_code[test_case_num][-1][:index + 1] + \
                                                  ' ' + str(
                        self.tasks[task_num][test_case_num]['input'][input_ctr]) + '\n'
                    input_ctr += 1
            new_code[test_case_num] += ['        return result____\n', 'f = Func()\n', 'f.func()']

        return new_code

    def run_code(self, code, task_num, case_num) -> bool:
        file = open(f'task.py', 'w', encoding='utf-8')
        for line in code:
            file.write(line)
        file.close()

        importlib.reload(task)
        time.sleep(1.5)
        result = task.Func().func()

        for i in range(len(result)):
            result[i] = str(result[i])

        return result == self.tasks[task_num][case_num]['output']
