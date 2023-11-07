from inkbs.client import generate_button
import uuid
from aiogram import Router, types
from models.chat import MessagePrivate

router = Router()

@router.inline_query()
async def empty_query(query: types.InlineQuery):
	text = query.query
	lst = text.split(" ")[-1]
	text = text.replace(lst, '')
	txt_len = len(text)
	txtlen = len(text.split(' '))
	if txtlen >= 2 and txt_len<=255:
		msg_id = str(uuid.uuid4())
		message = MessagePrivate.create(message_text=text, message_id = msg_id,userid=query.from_user.id, name = query.from_user.full_name,
                                        to_user=lst.replace('@',''))
		message.save()

		button = await generate_button(message.id)
		result = types.InlineQueryResultArticle(
            id=msg_id,
            title=f"Шепот | {txt_len}/255",
            input_message_content=types.InputTextMessageContent(
                message_text=f"Сообщение для {lst}, кол-во символов {txt_len}"+
                "\n\nТелеграм канал: https://t.me/RedFoxBotMakerchnl",
            ),
            reply_markup=button,
        )

		await query.answer(results=[result,])
	else:
		result = types.InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Шепот | {txt_len}/255",
            input_message_content=types.InputTextMessageContent(
                message_text=f"Сообщение для {lst}, кол-во символов {txt_len}",
            )
        )

		await query.answer(results=[result,])
