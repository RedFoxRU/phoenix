from aiogram import types

async def generate_button(id):
    button = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Посмотреть сообщение",
                    callback_data=f"whisper,{id}"
                )
            ]
        ]
    )
    return button