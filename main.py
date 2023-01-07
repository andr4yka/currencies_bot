import datetime
import hashlib
import logging
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InlineQueryResultArticle
from pycbrf import ExchangeRates
from config import TOKEN

logging.basicConfig(level=logging.INFO)
token = TOKEN

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
        id INTEGER
        )""")

    connec.commit()

    people_id = message.from_user.id
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_id = [message.from_user.id]
        cursor.execute("INSERT INTO users VALUES(?);", user_id)
        connec.commit()
    else:
        pass

    await message.reply("Привет! Я бот, который умеет переводить валюту по курсам, установленными Центробанком "
                        "России.\n\nНапиши /transfer и необходимую валюту ($, "
                        "€, "
                        "£, ₽ или ¥),\nНапример: /transfer 100$ (или $100).\n\nЕсли что ¥ - китайский юань, не путать "
                        "с японской иеной\n\nО всех технических неполадках "
                        "пиши "
                        "@andr4yka")


@dp.inline_handler()
async def inline_handler(query: InlineQuery):
    text = query.query or 'echo'
    title = 'Перевод валют'
    description = f'Перевести {text}'
    input_message_content = types.InputTextMessageContent(text)
    item = InlineQueryResultArticle(id=hashlib.md5(text.encode()).hexdigest(),
                                    title=title,
                                    description=description,
                                    input_message_content=input_message_content)
    item.title = title
    item.description = description
    item.input_message_content = input_message_content
    await bot.answer_inline_query(process_transfer_command, cache_time=1, is_personal=True, results=[item])


@dp.message_handler(commands=['transfer'])
async def process_transfer_command(message: types.Message):
    global a
    a = message.text[10:]
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
    yes = 0
    for i in a:
        if i == '$':
            yes += 1
        else:
            continue

    if yes > 1:
        result = 'Слишком много $, проверьте правильность ввода'
        return result

    if a[0] == '$':
        try:
            doll = int(a[1:])
            znach = doll * usd
            result = f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result
    elif a[-1] == '$':
        try:
            doll = int(a[:-1])
            znach = doll * usd
            result = f"{a} = {round(znach, 2)}₽\n{a} = {round(znach / eur, 2)}€\n{a} = {round(znach / gbp, 2)}£\n{a} = {round(znach * 10 / cny, 2)}¥"
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result


async def euros():
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
            result = f"{a} = {round(znach/10, 2)}₽\n{a} = {round(znach / 10 / usd, 2)}$\n{a} = {round(znach / 10 / eur, 2)}€\n{a} = {round(znach / 10 / gbp, 2)}£ "
            return result
        except ValueError:
            result = 'Ошибка ввода'
            return result


if __name__ == '__main__':
    executor.start_polling(dp)
