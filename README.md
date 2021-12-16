# Проект QABot

### Описание:
- Проект служит для автоматизированного тестирования python кода в дискорд каналах.
- Админы загружают задания с описанием и систему тестов.
- Другие участники отправляют свой код и смотрят кол-во пройденных тестов


### Технологический стек:
- python 3.9
- discord.py
- discord-slash-commands.py

### Инструкция по настройке проекта:
1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project QABot -> project interpreter)
4. Открыть терминал в PyCharm
5. **Проверить, что виртуальное окружение активировано**.
6. Обновить pip:
    ```bash
    pip install --upgrade pip
    ```
7. Установить в виртуальное окружение необходимые пакеты: 
    ```bash
    pip install -r requirements.txt
    ```
8. Создать конфигурацию запуска в PyCharm (файл `run.py`)

