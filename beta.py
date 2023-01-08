@dp.inline_handler()
async def inline_handler(query: InlineQuery, message: types.Message):
    a = query.query or 'вашу валюту'
    title = 'Перевод валют'
    description = f'Перевести {a}'
    input_message_content = types.InputTextMessageContent(a)
    item = InlineQueryResultArticle(id=hashlib.md5(a.encode()).hexdigest(),
                                    title=title,
                                    description=description,
                                    input_message_content=input_message_content)
    item.title = title
    item.description = description
    item.input_message_content = input_message_content
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

