#Весь юзербот является экспериментом: "Сможет ли нейросеть написать полноценный юзербот?". По чему-то писать ему: @rav1non (телеграм)

from pyrogram.types import Message
from pyrogram.types import ChatPermissions
import time
import asyncio
from pyrogram import Client, filters , types
from random import choice
import random
import requests
import platform
import psutil
from bs4 import BeautifulSoup
import os
import sys
from pyrogram.types import User
from datetime import datetime
import pyowm
import qrcode
from transliterate import translit

afk_mode = False
afk_reason = ""
afk_start_time = 0
last_command_time = {}
api_url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&limit=1&q=komaru'
url = "https://x0.at/5wuk.mp4"

with open("kub.info", "r") as file:
    lines = file.readlines()
    api_id = int(lines[0].strip())
    api_hash = lines[1].strip()
    my_user_id = int(lines[2].strip())
    prefix = lines[3].strip()
    api_owm = lines[4].strip()

app = Client("kub", api_hash=api_hash, api_id=api_id)
start_time = datetime.now()

@app.on_message(filters.me & filters.command("afk", prefixes=prefix) & filters.me)
def set_afk_mode(_, message):
    global afk_mode, afk_reason, afk_start_time
    afk_mode = True
    afk_reason = " ".join(message.command[1:])
    afk_start_time = datetime.now()
    message.edit_text("```СООБЩЕНИЕ ОТ KUB\n😴AFK включено!```")


@app.on_message(filters.mentioned)
def check_afk(client, message):
    if afk_mode:
        current_time = datetime.now()
        time_diff = current_time - afk_start_time
        message.reply_text(f"```СООБЩЕНИЕ ОТ KUB\n💤Юзер сейчас в AFK. \nВремя AFK - {time_diff} \nПричина - {afk_reason}```")


# Команда "afkoff"
@app.on_message(filters.me & filters.command("afkoff", prefixes=prefix) & filters.me)
def unset_afk_mode(client, message):
    global afk_mode
    afk_mode = False
    message.edit_text("```СООБЩЕНИЕ ОТ KUB\n🥱AFK выключено!```")

@app.on_message(filters.command("kuboff", prefixes=prefix) & filters.me)
async def kuboff_command(client, message):
    try:
        # Вычисление времени работы бота
        uptime = datetime.now() - start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours} часов, {minutes} минут, {seconds} секунд"
        
        # Формирование текста сообщения
        shutdown_message = f"```Сообщение от KUB:\n💤 Юзербот успешно выключен. Он проработал {uptime_str}.```"

        # Логирование
        print(f"Shutdown message: {shutdown_message}")

        # Проверка, что сообщение не пустое и отправка новой версии
        if shutdown_message.strip():
            await message.edit_text(shutdown_message)
        else:
            print("Сообщение пустое")
            await message.reply("Произошла ошибка: сообщение пустое.")
            return

        # Немного подождать, чтобы сообщение успело измениться
        await asyncio.sleep(3)

        # Остановить бота
        await app.stop()
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        
@app.on_message(filters.command("swap", prefixes=prefix) & filters.me)
def swap(client, message):
    original_text = message.reply_to_message.text
    swapped_text = swap_layout(original_text)
    message.edit_text(swapped_text)

eng_to_rus = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,.`",
    "йцукенгшщзхъфывапролджэячсмитьбюё"
)
rus_to_eng = str.maketrans(
    "йцукенгшщзхъфывапролджэячсмитьбюё",
    "qwertyuiop[]asdfghjkl;'zxcvbnm,.`"
)


def swap_layout(text):
    words = text.split()
    swapped_words = []
    for word in words:
        if word.isupper():
            swapped_word = word.lower().translate(rus_to_eng if 'а' <= word.lower()[0] <= 'я' or word.lower()[0] == 'ё' else eng_to_rus)
            swapped_words.append(swapped_word.upper())
        else:
            swapped_words.append(word.translate(rus_to_eng if 'а' <= word.lower()[0] <= 'я' or word.lower()[0] == 'ё' else eng_to_rus))
    return ' '.join(swapped_words)

@app.on_message(filters.command("tagall", prefixes=prefix) & filters.group & filters.me)
def tag_all_members(client, message):
    chat_id = message.chat.id
    members = client.get_chat_members(chat_id)
    
    # Извлекаем имена всех участников чата
    usernames = [member.user.username for member in members if member.user.username]
    user_mentions = " ".join([f"@{username}" for username in usernames])
    
    # Отправляем ответное сообщение с упоминанием всех участников
    client.send_message(chat_id,f"```\nОтметил всех:```{user_mentions}")
    
    # Скрытие команды "+tagall"
    message.delete()

@app.on_message(filters.command("mqr", prefixes=prefix) & filters.me)
async def generate_qr_code(client, message):
    # Разбиваем сообщение на части, чтобы получить текст после "+mqr"
    command, _, text = message.text.partition(" ")

    # Генерируем QR-код с использованием текста
    qr = qrcode.make(text)

    # Сохраняем QR-код как файл
    qr_file = "qr_code.png"
    qr.save(qr_file)

    # Отправляем файл в чат
    await client.send_photo(
        chat_id=message.chat.id,
        photo=qr_file
    )

    # Удаляем временный файл QR-кода
    os.remove(qr_file)
    await message.delete()
    
@app.on_message(filters.command("rrot5", prefixes=prefix) & filters.me)
def encrypt_text(client, message):
    # Получаем текст после команды
    text = message.text.split(maxsplit=1)[1]
    encrypted_text = ''

    for char in text:
        if char.isalpha():
            # Получаем код символа
            code = ord(char)
            # Шифруем символы русского алфавита
            if 'а' <= char <= 'я':
                code = (code - ord('а') + 5) % 32 + ord('а')
            elif 'А' <= char <= 'Я':
                code = (code - ord('А') + 5) % 32 + ord('А')
            char = chr(code)
        encrypted_text += char

    # Отправляем зашифрованный текст в ответ
    message.edit_text("```\nЗашифровал текст:```\n " + '`' + encrypted_text + '`')

@app.on_message(filters.command("drrot5", prefixes=prefix) & filters.me)
def decrypt_text(client, message):
    # Получаем текст после команды
    text = message.text.split(maxsplit=1)[1]
    decrypted_text = ''

    for char in text:
        if char.isalpha():
            # Получаем код символа
            code = ord(char)
            # Расшифровываем символы русского алфавита
            if 'а' <= char <= 'я':
                code = (code - ord('а') - 5) % 32 + ord('а')
            elif 'А' <= char <= 'Я':
                code = (code - ord('А') - 5) % 32 + ord('А')
            char = chr(code)
        decrypted_text += char

    # Отправляем расшифрованный текст в ответ
    message.edit_text("```\nРасшифровал текст:```\n " + '`' + decrypted_text + '`')
    
@app.on_message(filters.command("help", prefixes=prefix) & filters.me)
def help_command(client, message):
    prf = prefix
    message.edit("```ПOМОЩЬ KUB\nВаш префикс: "f"{prf}\n\nОбычных команд: 19\n\nПолу-команд: 3\n\nОбычные команды:\n1. "f"{prf}help - помощь по использованию юзербота\n2. "f"{prf}scrkom - почесать Комару\n3. "f"{prf}kping - Пинг телеграма\n4. "f"{prf}calc - вычисляет как калькулятор. + это сложение, - вычитание, * умножение, / деление, **  степень\n5. "f"{prf}iub - информация о юб\n6. "f"{prf}randkom - отправляет рандомную гифку с комару (иногда попадается какая-то аниме фигня)\n7. "f"{prf}sysinf - отправляет информацию о системе\n8. "f"{prf}upk - показывает сколько времени работает юзербот\n9. "f"{prf}wiki - отправляет статью с Википедии по запросу (немного кривая команда, потом будет фикс)\n10. "f"{prf}rel - перезапускает юзербота\n11. "f"{prf}weather город - выдаёт прогноз погоды в этом городе\n12. "f"{prf}rrot5 текст НА РУССКОМ ЯЗЫКЕ - шифрует текст в шифр ROT5\n13. "f"{prf}drrot5  - расшифровывает текст из шифра ROT5 (drrot5 зашифрованный текст)\n14. "f"{prf}mqr текст - делает qr код содержащий текст\n15. "f"{prf}tagall - отмечает всех участников чата\n16. "f"{prf}kuboff - выключает юзербот\n17. "f"{prf}swap - (ответом на сообщение) переключает раскладку сообщения (с английской на русскую\n18. "f"{prf}afk - переводит вас в AFK. Что бы отключить  AFK напишите команду afkoff (спасибо: @telery_userbot2)\n19. .prefix - изменяет префикс KUB (спасибо: @telery_userbot2)\n\nПолу-команды:\n1. "f"{prf}rev - переворачивает сообщение (привет - тевирп)\n2. "f"{prf}version - показывает какая у вас версия юзербота и где её скачать\n3. "f"{prf}dev - отправляет юзернейм разработчика```")
    
@app.on_message(filters.command("prefix", prefixes=".") & filters.me)
def change_prefix_command(command, message):
    if len(message.command) > 1:
        new_prefix = message.command[1]
        change_prefix(new_prefix)
        message.edit_text(f"```СООБЩЕНИЕ ОТ KUB\nВаш префикс изменён. Перезапустите юзербота командой rel, чтобы префикс изменился.```")
    elif command.startswith(".prefix"):
        with open("userbot.info", "r") as file:
            prefix = file.readlines()[3].strip()
        message.edit_text(f"```СООБЩЕНИЕ ОТ KUB/nВаш префикс:\n{prefix}```")


def is_allowed(user_id):
    with open("kub.info", "r") as file:
        first_line = file.readline()
        return str(user_id) in first_line


def change_prefix(new_prefix):
    with open("kub.info", "r+") as file:
        lines = file.readlines()
        lines[3] = new_prefix + "\n"
        file.seek(0)
        file.writelines(lines)
        file.truncate()
    
@app.on_message(filters.command("rev", prefixes=prefix) & filters.me)
def reverse_text(client, message):

    text = message.text.split(" ", 1)[1]
    
    reversed_text = text[::-1]
   
    message.edit_text(reversed_text)
    
@app.on_message(filters.command("dev", prefixes=prefix) & filters.me)
def dev_command(client, message):
    message.edit("**РАЗРАБОТЧИК KUB**:\n@rav1non")

@app.on_message(filters.command("weather", prefixes=prefix) & filters.me)
async def get_weather(bot, message):
    chat_id = message.chat.id
    city = " ".join(message.command[1:])
    if not city:
        await bot.send_message(chat_id, '```Сообщение от KUB\nПожалуйста, укажите город```')
        await message.delete()
        return
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_owm}&units=metric'
    response = requests.get(weather_url)
    weather_data = response.json()
    if weather_data.get("cod") != 404:
        weather_info = f"```ПОГОДА ОТ KUB В ГОРОДЕ {city}\n☁️ Погода в городе {city}:\n🌡 Температура: {weather_data['main']['temp']}°C\n🧥 Ощущается как:  {weather_data['main']['feels_like']}°C\n💧 Влажность: {weather_data['main']['humidity']}%\n🕡  Давление: {weather_data['main']['pressure']}гПа\n💨 Скорость ветра: {weather_data['wind']['speed']}м/с```"
        await bot.send_message(chat_id, weather_info)
        await message.delete()
    else:
        await bot.send_message(chat_id, '```Ошибка\nГород не найден.Пожалуйста, укажите корректное название города.```')

async def restart_bot(bot, message):
    await bot.send_message(message.chat.id, "```Сообщение от KUB\nKUB перезапускается```")
    await message.delete()
    os.execl(sys.executable, sys.executable, *sys.argv)

@app.on_message(filters.command("rel", prefixes=prefix) & filters.me)
async def handle_restart_command(bot, message):
    await restart_bot(bot, message)
    
@app.on_message(filters.command("spam", prefixes=prefix) & filters.me)
async def spam_message(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text # Получаем текст сообщения, на которое отвечаем
        count = 10 # По умолчанию отправляем только одно сообщение
    elif len(message.command) == 2:
        count = int(message.command[1])
        text = None
    else:
        count, text = message.command[1], message.command[2]
        count = int(count)
        
    if text is not None:
        # Отправляем текст столько раз, сколько указано в числе
        for _ in range(count):
            await app.send_message(message.chat.id, text)
            await asyncio.sleep(0)
        await message.delete()
    
@app.on_message(filters.command("version", prefixes=prefix) & filters.me)
def version_command(client, message):
    message.edit("**ВЕРСИЯ 1.0 ДЛЯ ВСЕХ 🐈 **")

@app.on_message(filters.command("scrkom", prefixes=prefix) & filters.user([1299931185, 6400632128, 1499962079, 1325079151, 1891411470]))
async def edit_message(app: Client, message: Message):
    url = "https://x0.at/6D5G.mp4"
    msg = await app.send_animation(message.chat.id, url, caption="**ВЫ ПОЧЕСАЛИ КОМАРУ**")
    await message.delete()

@app.on_message(filters.command("kping", prefixes=prefix) & filters.me)
def ping(client, message):
    ping = None
    if len(message.text.split(' ', 1)) > 1:
        ping = message.text.split(' ', 1)[1]
    start_time = time.perf_counter_ns()
    message.edit_text("🚀")
    end_time = time.perf_counter_ns()
    ping_time = (end_time - start_time) / 1e6
    if ping:
        message.edit_text(
            f"```KUB Ping\n🐈 Скорость отклика Telegram: {ping} ms\n```"
        )
    else:
        message.edit_text(
            f"```KUB Ping\n🐈 Скорость отклика Telegram: {ping_time:.3f} ms\n```"
        )
        
@app.on_message(filters.command("calc", prefixes=prefix) & filters.me)
async def calculatorblya(client, message):
    if message.text.startswith("+calc"):
        expression = message.text[6:]
        if len(expression) > 0:
            try:
                result = eval(expression)
                await message.edit_text(f"```Калькулятор\nРезультат: {result}```")
            except Exception as e:
                await message.edit_text(f"```Ошибка\n{e}```")
        else:
            await message.edit_text("```Пожалуйста, введите выражение после команды +calc.```")
@app.on_message(filters.command("iub", prefixes=prefix) & filters.me)
async def ping(client, message):
    ping = None
    if len(message.text.split(' ', 1)) > 1:
        ping = message.text.split(' ', 1)[1]
    start_time = time.perf_counter_ns()
    
    await message.edit_text("🚀")
    
    end_time = time.perf_counter_ns()
    ping_time = (end_time - start_time) / 1e6
    
    if ping:
        msg = await client.send_photo(message.chat.id, url, caption=f"**KUB**n**Version: 1.3 for dev 🐈**n**Developer:** @rav1non\n**Telegram ping:** {ping} ms")
    else:
        msg = await client.send_photo(message.chat.id, url, caption=f"**KUB**\n**Version: 1.3 for dev 🐈**\n**Developer:** @rav1non\n**Telegram ping:** {ping_time:.3f} ms")
    
    await message.delete()
    
def get_random_kom_gif():
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            gif_url = data['results'][0]['media'][0]['gif']['url']
            return gif_url
        else:
            return None
    else:
        return None

@app.on_message(filters.command("randkom", prefixes=prefix) & filters.me)
async def send_random_kom_gif(client, message):
    gif_url = get_random_kom_gif()
    if gif_url:
        await client.send_animation(message.chat.id, animation=gif_url)
        await message.delete()
    else:
        await client.send_message(message.chat.id, "Простите, но я не смог найти гиф с Комару.")

def get_system_info():
    system_info = "**Операционная система: `{}`**\n".format(platform.system())
    system_info += "**Процессор: `{}`**\n".format(platform.processor())
    virtual_memory = psutil.virtual_memory()
    system_info += "**Всего оперативной памяти: `{}` GB**\n".format(round(virtual_memory.total / (1024.0 ** 3), 2))
    system_info += "**Занято оперативной памяти: `{}` GB**\n".format(round(virtual_memory.used / (1024.0 ** 3), 2))
    return system_info
    
@app.on_message(filters.command("sysinf", prefixes=prefix) & filters.me)
async def send_system_info(client, message):
    sys_info = get_system_info()
    await client.send_message(message.chat.id, sys_info)
    await message.delete()

start_time = datetime.now()

@app.on_message(filters.command("upk", prefixes=prefix) & filters.me)
def upk(client, message):
    current_time = datetime.now()
    uptime = current_time - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    message.edit_text(f"```Uptime KUB\nKUB работает {days} дней, {hours} часов, {minutes} минут и {seconds} секунд```")

@app.on_message(filters.command("wiki", prefixes=prefix) & filters.me)
def get_wiki(client, message):
    query = message.text.split(' ', 1)[1]
    url = f"https://ru.wikipedia.org/wiki/{query}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        result_div = soup.find('div', class_='mw-parser-output')
        if result_div:
            paragraphs = result_div.find_all('p')
            result = ""
            for p in paragraphs:
                text = p.get_text().strip()
                if len(result + text) < 4096:
                    result += text + "\n"
                else:
                    break
            if result:
                message.edit_text(result)
            else:
                message.edit_text("Извините, не найдено результатов по вашему запросу")
        else:
            message.edit_text("Извините, не найдено результатов по вашему запросу")
    else:
        message.edit_text("Извините, не найдено результатов по вашему запросу")
        
print("Бот запущен!")
app.run()
