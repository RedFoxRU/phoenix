from datetime import datetime
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message

from models.chat import Chat, User


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text and event.text[0] != '/':
            chat, _c = Chat.get_or_create(tgid=event.chat.id)
            chat.title = event.chat.title
            chat.save()
            user, _u = User.get_or_create(tgid=event.from_user.id, chat_id=event.chat.id)
            user.username        = event.from_user.username
            user.last_message    = datetime.now()
            user.total_messages += 1
            user.save()
        return await handler(event, data)