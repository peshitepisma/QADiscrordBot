from channels import Base


class Test(Base):

    async def run(self):
        if self.message.content.startswith('!test'):
            result_string = ''
            await self.message.delete()
            if self.message.content.find('result____') != -1:
                await self.message.channel.send('В вашем коде обнаружена переменная с именем "result____".'
                                                ' Переименуйте её для проверки')
                return

            if self.message.content.find('func(') != -1:
                await self.message.channel.send('В вашем коде обнаружена функция или метод "func". Исправь пж')
            text = self.message.content.split('\n')
            msg = text[0].split()
            code = text[1:]
            if msg[0] == '!test':
                if msg[1].isdigit():
                    if code:
                        await self.message.channel.send("Тестирую. Попей чаю 🍵")
                        code = self.bot.transform_code(code, int(msg[1]))
                        for i in range(len(code)):
                            if self.bot.run_code(code[i], int(msg[1]), i):
                                result_string += f'✅ Тест {i} - успешно\n'
                            else:
                                result_string += f'❌ Тест {i} - неверный ответ\n'

                        await self.message.channel.send(f'```\n{result_string}```')
