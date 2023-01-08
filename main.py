import sqlite3
import pycbrf
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InlineQueryResultArticle
from pycbrf import ExchangeRates
import sqlite3
import logging
import hashlib
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
    connec = sqlite3.connect('users.db')
    cursor = connec.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
        username NOT NULL,
        user_id INTEGER
        )""")

    connec.commit()

    user_id = [message.from_user.id]
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES('{message.from_user.username}', '{message.from_user.id}')")
        connec.commit()
    else:
        pass

    if message.from_user.username is None:
        await message.reply("Привет! Я бот, который умеет переводить валюту по курсам, установленными Центробанком "
                            "России.\n\nНапиши /transfer и необходимую валюту ($, "
                            "€, "
                            "£, ₽ или ¥),\nНапример: <code>/transfer 100$</code> (или $100).\n\nЕсли что ¥ - китайский "
                            "юань, не путать "
                            "с японской иеной.")
        await message.answer("""Дорогой пользователь, я не могу определить твой никнейм. Пожалуйста, установи никнейм в настройках аккаунта, иначе я не смогу сохранить твои данные в базе данных\n\nP.S. Я не шпион, подосланный Пентагоном (@andr4yka, автор этого бота, тоже не шпион), и я не собираюсь отслеживать твои действия и отсылать их на куда-либо. Я просто бот, который хочет помочь тебе с конвертацией валют.\n\nP.P.S И да, каждый раз когда ты будешь писать мне /start, я буду тебе напоминать о том, что ты не установил никнейм (пока ты его не установишь).\n\nУ тебя есть удивительная возможность поблагодарить разработчика за это напоминание, написав ему в личку пару приятных слов.""")
    else:
        await message.reply("Привет! Я бот, который умеет переводить валюту по курсам, установленными Центробанком "
                            "России.\n\nНапиши /transfer и необходимую валюту ($, "
                            "€, "
                            "£, ₽ или ¥),\nНапример: <code>/transfer 100$</code> (или $100).\n\nЕсли что ¥ - китайский "
                            "юань, не путать "
                            "с японской иеной\n\nО всех технических неполадках "
                            "пиши "
                            "@andr4yka")
    connec.close()


@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    for chat_member in message.new_chat_members:
        if chat_member.id == bot_id:
            await message.answer("""""")


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


async def rubles():
    # Проверка на корректное наличие валюты
    yes = 0
    for i in a:
        if i == b[3]:
            yes += 1
        else:
            continue

    if yes > 1:
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
    yes = 0
    for i in a:
        if i == '€':
            yes += 1
        else:
            continue

    if yes > 1:
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
    yes = 0
    for i in a:
        if i == '£':
            yes += 1
        else:
            continue

    if yes > 1:
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
    yes = 0
    for i in a:
        if i == '¥':
            yes += 1
        else:
            continue

    if yes > 1:
        result = 'Слишком много ¥, проверьте правильность ввода'
        return result

    if a[0] == '¥':
        try:
            yuan = int(a[1:])
            znach = yuan * cny
            result = f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / usd, 2)}$\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£ "
            return result

        except ValueError:
            result = 'Ошибка ввода'
            return result
    elif a[-1] == '¥':
        try:
            yuan = int(a[:-1])
            znach = yuan * cny
            result = f"{a} = {round(znach / 10, 2)}₽\n{a} = {round(znach / 10 / usd, 2)}$\n{a} = {round(znach / 10 / eur, 2)}€\n{a} = {round(znach / 10 / gbp, 2)}£ "
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result


if __name__ == '__main__':
    executor.start_polling(dp)
