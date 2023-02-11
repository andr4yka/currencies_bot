import datetime
import logging
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from pycbrf import ExchangeRates

import config

logging.basicConfig(level=logging.INFO)
token = config.token

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

rates = ExchangeRates(datetime.date.today())

usd = rates['USD'].value
eur = rates['EUR'].value
gbp = rates['GBP'].value
cny = rates['CNY'].value

b = ['$', '€', '£', '₽', '¥']


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    file = open('users.txt', 'r', encoding='utf-8')
    if f"{message.from_user.username} ({message.from_user.id})" in file.read():
        pass
    else:
        with open('users.txt', 'a', encoding='utf-8') as file:
            file.write(f"{message.from_user.username} ({message.from_user.id})\n")
    await message.reply("Привет! Я бот, который умеет переводить валюту по курсам, установленными Центробанком "
                        "России.\n\nНапиши <code>/transfer</code> и необходимую валюту (<code>$</code>, "
                        "<code>€</code>, "
                        "<code>£</code>, <code>₽</code> или <code>¥</code>),\nНапример: <code>/transfer 100$</code> (или $100).\n\nЕсли что ¥ - китайский "
                        "юань, не путать "
                        "с японской иеной\n\nО всех технических неполадках "
                        "пиши "
                        "@andr4yka")


@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    bot.obj = await bot.get_me()
    bot.id = bot.obj.id
    for chat_member in message.new_chat_members:
        if chat_member.id == bot.id:
            await message.answer("Привет! Я бот, который умеет переводить валюту по курсам, установленными Центробанком"
                                 "России.\n\nНапиши <code>/transfer</code> и необходимую валюту ($, "
                                 "€, "
                                 "£, ₽ или ¥),\nНапример: <code>/transfer 100$</code> (или $100).\n\nЕсли что ¥ - китайский "
                                 "юань, не путать "
                                 "с японской иеной\n\nО всех технических неполадках "
                                 "пиши "
                                 "@andr4yka")


@dp.message_handler(commands=['transfer'])
async def process_transfer_command(message: types.Message):
    global a
    a = message.text[10:]  # Обрезаем команду /transfer
    if b[0] in a:
        await message.reply(await dollars())
    elif b[1] in a:
        await message.reply(await euros())
    elif b[2] in a:
        await message.reply(await pounds())
    elif b[3] in a:
        await message.reply(await rubles())
    elif b[4] in a:
        await message.reply(await yuan())
    else:
        await message.reply('Отсутствует валюта, проверьте правильность ввода')

    file = open('users.txt', 'r', encoding='utf-8')
    if f"{message.from_user.username} ({message.from_user.id})" in file.read():
        pass
    else:
        with open('users.txt', 'a', encoding='utf-8') as file:
            file.write(f"{message.from_user.username} (https://web.telegram.org/z/#{message.from_user.id})\n")


#    connec = sqlite3.connect('users.db')
#    cursor = connec.cursor()

#    cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
#        username NOT NULL,
#        user_id INTEGER
#        )""")

#    connec.commit()
#
#    user_id = [message.from_user.id]
#    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
#    if cursor.fetchone() is None:
#        cursor.execute(f"INSERT INTO users VALUES('{message.from_user.username}', '{message.from_user.id}')")
#        connec.commit()
#    else:
#        pass


async def rubles():
    # Проверка на корректное наличие валюты
    err = 0
    for i in a:
        if i == b[3]:
            err += 1
        else:
            continue

    if err > 1:
        result = 'Слишком много ₽, проверьте правильность ввода'
        return result

    if a[0] == '₽':
        try:
            rub = int(a[1:])
            znach = rub
            result = f"{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result
    elif a[-1] == '₽':
        try:
            rub = int(a[:-1])
            znach = rub
            result = f"{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£\n {a} = {round(znach * 10 / cny, 2)}¥"
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result


async def dollars():
    # Проверка на корректное наличие валюты
    if a[0] == b[0]:
        try:
            doll = int(a[1:])
            znach = doll * usd
            result = f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result
    elif a[-1] == b[0]:
        try:
            doll = int(a[:-1])
            znach = doll * usd
            result = f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result


async def euros():
    # Проверка на корректное наличие валюты
    err = 0
    for i in a:
        if i == '€':
            err += 1
        else:
            continue

    if err > 1:
        return 'Слишком много €, проверьте правильность ввода'
    if a[0] == '€':
        try:
            euro = int(a[1:])
            znach = euro * eur
            return f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"

        except ValueError:
            return 'Ошибка ввода'

    elif a[-1] == '€':
        try:
            euro = int(a[:-1])
            znach = euro * eur
            return f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"
        except ValueError:
            return 'Ошибка ввода'


async def pounds():
    # Проверка на корректное наличие валюты
    err = 0
    for i in a:
        if i == '£':
            err += 1
        else:
            continue

    if err > 1:
        return 'Слишком много £, проверьте правильность ввода'

    if a[0] == '£':
        try:
            pound = int(a[1:])
            znach = pound * gbp

            return f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach * 10 / cny, 2)}¥"

        except ValueError:
            return 'Ошибка ввода'
    elif a[-1] == '£':
        try:
            pound = int(a[:-1])
            znach = pound * gbp
            return f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach * 10 / cny, 2)}¥"
        except ValueError:
            return 'Ошибка ввода'


async def yuan():
    # Проверка на корректное наличие валюты
    err = 0
    for i in a:
        if i == '¥':
            err += 1
        else:
            continue

    if err > 1:
        result = 'Слишком много ¥, проверьте правильность ввода'
        return result

    if a[0] == '¥':
        try:
            yuan = int(a[1:])
            znach = yuan * cny
            result = f"{a} = {round(znach , 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£ "
            return result

        except ValueError:
            result = 'Ошибка ввода'
            return result
    elif a[-1] == '¥':
        try:
            yuan = int(a[:-1])
            znach = yuan * cny
            result = f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£ "
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result


if __name__ == '__main__':
    executor.start_polling(dp)
