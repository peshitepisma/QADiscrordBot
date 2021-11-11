import time

import discord
import importlib
import os

client = discord.Client()

tasks = []

for file in os.listdir('task'):
    tasks.append([])
    f = open('task/' + file)

    ctr = 0
    for line in f:
        if ctr % 2 == 0:
            tasks[-1].append({'input': line.split()})

        else:
            tasks[-1][-1]['output'] = line.split()

        ctr += 1

    f.close()

@client.event
async def on_ready():
    pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == 'test_bot_mgmt':
        if message.content.startswith('!add_task'):
            tasks.append([])
            fl = open('task/' + str(len(tasks) - 1) + '.txt', 'w')
            fl.close()
            await message.channel.send(f'Добавлено задание номер {len(tasks) - 1}')
        if message.content.startswith('!add_test'):
            msg = message.content.split()
            task_num = int(msg[1])

            msg = message.content.split('\n')
            input = msg[1]
            output = msg[2]

            fl = open('task/' + str(task_num) + '.txt', 'a')
            fl.write(input + '\n')
            fl.write(output + '\n')
            fl.close()

            tasks[task_num].append({'input': input, 'output': output})
            await message.channel.send(f'Добавлен тесткейс в задание номер {task_num}')
        if message.content.startswith('!remove_test'):
            msg = message.content.split()
            task_num = int(msg[1])
            test_num = int(msg[2])

            del tasks[task_num][test_num]

            fl = open('task/' + msg[1] + '.txt', 'r')
            data = fl.readlines()
            fl.close()

            fl = open('task/' + msg[1] + '.txt', 'w')
            for i in range(len(data)):
                if i == test_num or i == test_num + 1:
                    continue

                fl.write(data[i])

            fl.close()

            await message.channel.send(f'Удален тесткейс в задании номер {task_num}')
        if message.content.startswith('!clear_tests'):
            msg = message.content.split()
            tasks[int(msg[1])].clear()

            fl = open('task/' + msg[1] + '.txt', 'w')
            fl.close()

            await message.channel.send(f'Удалены все тесткейсы задания номер {msg[1]}')
        elif message.content.startswith('!clear'):
            tasks.clear()
            files = []
            for fl in os.listdir('task'):
                os.remove(f'task/{fl}')

            await message.channel.send(f'Список заданий очищен')
    if message.channel.name == 'test_bot_channel':
        if message.content.startswith('!test'):
            result_string = ''
            await message.delete()
            if message.content.find('result____') != -1:
                await message.channel.send('В вашем коде обнаружена переменная с именем "result____".'
                                           ' Переименуйте её для проверки')
                return

            if message.content.find('func(') != -1:
                await message.channel.send('В вашем коде обнаружена функция или метод "func". Переименуйте для проверки')
            text = message.content.split('\n')
            msg = text[0].split()
            code = text[1:]
            if msg[0] == '!test':
                if msg[1].isdigit():
                    if len(code) != 0:
                        code = transform_code(code, int(msg[1]))
                        for i in range(len(code)):
                            if run_code(code[i], int(msg[1]), i):
                                result_string += f'✅ Тест {i} - успешно\n'

                            else:
                                result_string += f'❌ Тест {i} - неверный ответ\n'

                        await message.channel.send('```\n' + result_string + '```')


def transform_code(code, task_num):
    new_code = []
    for test_case_num in range(len(tasks[task_num])):
        new_code.append([])
        new_code[test_case_num].append('class Func:\n')
        new_code[test_case_num].append('    def func(self):\n')
        new_code[test_case_num].append('        result____ = []\n')
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
                                              ' ' + str(tasks[task_num][test_case_num]['input'][input_ctr]) + '\n'
                input_ctr += 1

        new_code[test_case_num].append('        return result____\n')
        new_code[test_case_num].append('f = Func()\n')
        new_code[test_case_num].append('f.func()')

    return new_code


def run_code(code, task_num, case_num):
    file = open(f'task.py', 'w', encoding='utf-8')
    for line in code:
        file.write(line)

    file.close()

    import task

    importlib.reload(task)
    time.sleep(0.5)
    result = task.Func()
    result = result.func()

    for i in range(len(result)):
        result[i] = str(result[i])

    return result == tasks[task_num][case_num]['output']


client.run('OTA4MDQ4OTMzODkxMjIzNTcy.YYwEeA.RJIYZSHInFrDgd16hIoPDdAulwc')
