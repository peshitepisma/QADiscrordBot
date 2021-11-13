import discord
import task
import time
import importlib
from channels import Task, Test
from db import Database


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.create()
        self.channels = {
            'test_bot_mgmt': Task,
            'test_bot_channel': Test,
        }

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.channel.name in self.channels.keys():
            await self.channels[message.channel.name](bot=self, message=message).run()

    def transform_code(self, code, task):
        new_code = []
        for test_case_num in range(len(task.tests)):
            new_code.append([])
            new_code[test_case_num] += ['class Func:\n', '    def func(self):\n', '        result____ = []\n']
            input_ctr = 0
            test_input = task.tests[test_case_num].input.strip().split()
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
                    new_code[test_case_num][-1] = f'{new_code[test_case_num][-1][:index + 1]} {test_input[input_ctr]}\n'
                    input_ctr += 1
            new_code[test_case_num] += ['        return result____\n', 'f = Func()\n', 'f.func()']

        return new_code

    def run_code(self, code, test) -> bool:
        file = open(f'task.py', 'w', encoding='utf-8')
        for line in code:
            file.write(line)
        file.close()

        importlib.reload(task)
        time.sleep(1.5)
        result = task.Func().func()

        for i in range(len(result)):
            result[i] = str(result[i])

        return result == test.output.strip().split()
