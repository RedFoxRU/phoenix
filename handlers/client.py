from datetime import datetime
from random import randint
from bot import dp, states, bot
from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from filters import RolePlayFilter
from models.chat import BanStick, User, Chat
from texts import client as text
from fuzzywuzzy import fuzz
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from utils import client

@dp.message_handler(commands=['online'])
async def online_handler(message: types.Message):
	await message.reply(text.ONLINE_ME)

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
	chat, _c = Chat.get_or_create(tgid=message.chat.id)
	chat.title = message.chat.title
	chat.save()
	user, _u = User.get_or_create(tgid=message.from_user.id, chat_id=message.chat.id)
	user.addDate = datetime.now()
	user.save()
	if _u:
		await message.reply(f"{text.RULE_NEW_MEMBER.format(name=message.from_user.full_name)}\n{text.RULES}")
	else:
		await message.reply(f"{text.RULE_OLD_NEW_MEMBER.format(name=message.from_user.full_name)}\n{text.RULES}")

@dp.message_handler(content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def left_members_handler(message: types.Message):
    await message.reply(text.MEMBER_LEFT.format(name=message.from_user.full_name))


@dp.message_handler(commands=['inactive'])
async def inactive_top(message: types.Message):
	users = User.select().where(User.chat == message.chat.id).order_by(User.last_message)
	outText = 'Топ инактивов:\n\n'
	i = 1
	for user in users:
		try:
			k = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user.tgid)
			if k.status in ['member', 'creator', 'administrator']:
				if i <= 10:
					outText += f"{i}) [{k.user.full_name.replace('ㅤ', '')}](t.me/{user.username}) {user.last_message.strftime('%Y-%m-%d %H:%M:%S')}\n"
					i+=1
				else:
					break
			else:
				continue
		except:
			pass
	await message.answer(outText, parse_mode='markdown')

@dp.message_handler(commands=['addtop'])
async def inactive_top(message: types.Message):
	users = User.select().where(User.chat == message.chat.id).order_by(User.addDate.desc())
	outText = 'Топ новичков:\n\n'
	i = 1
	for user in users:
		try:
			k = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user.tgid)
			if k.status in ['creator', 'administrator', 'member', 'restricted']:
				if i <= 10:
					outText += f"{i}) [{k.user.full_name.replace('ㅤ', '')}](t.me/{user.username}) *{user.addDate}* добавили\n"
					i+=1
				else:
					break
			else:
				continue
		except:
			pass
	await message.answer(outText, parse_mode='markdown')
	

@dp.message_handler(commands=['ruser'], state='*')
async def ruser_handler(message: types.Message, state: FSMContext):
	# await message.delete()
	users = User.select().where(User.chat == message.chat.id)
	users_ = []
	for user in users:
		_user = await bot.get_chat_member(message.chat.id, user.tgid)
		status = _user.status.lower()
		if status in ['owner', 'administrator', 'member', 'restricted']:
			users_.append([user.tgid, _user.user.username])
	for user in users_:
		ruser = users_[randint(0,len(users_)-1)]
		if ruser[0] == 285635206:
			continue
		user_state = dp.current_state(user=ruser[0], chat=message.chat.id)
		if await state.get_data('ruser'):
			ruser = await state.get_data('ruser')
			await message.reply(f'Вы уже должны были поменяться с @{ruser["ruser"][1]}')
			return
		if await user_state.get_data('ruser'):
			continue
		await state.set_data({'ruser':ruser})
		await user_state.set_data({'ruser':[message.from_user.id, message.from_user.username]})
		await message.reply(f'Вы взаимно меняетесь аватарками и никами с @{ruser[1]}')
		return
	else:
		await message.reply(f'Нехватка людей, попробуйте позже')
     
    
@dp.message_handler(commands=['actived'])
async def inactive_top(message: types.Message):
	users = User.select().where(User.chat == message.chat.id).order_by(User.total_messages.desc())
	outText = 'Топ активов (сообщений за неделю):\n\n'
	i = 1
	for user in users:
		try:
			k = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user.tgid)
			if k.status in ['creator', 'administrator', 'member', 'restricted']:
				if i <= 10:
					outText += f"{i}) [{k.user.full_name.replace('ㅤ', '')}](t.me/{user.username}) *{user.total_messages}* сообщений\n"
					i+=1
				else:
					break
			else:
				continue
		except:
			pass
	await message.answer(outText, parse_mode='markdown')



@dp.message_handler(commands=['rule'])
async def getRules(message: types.Message):
	await message.answer(text.RULES, parse_mode='markdown')

@dp.message_handler(content_types=[types.ContentType.STICKER])
async def message_stick_handler(message: types.Message):
	stick = BanStick.get_or_none((BanStick.emoji == message.sticker.emoji)&(BanStick.file_size == message.sticker.file_size)&(BanStick.height == message.sticker.height)&(BanStick.chat == message.chat.id))
	# emoji=message.reply_to_message.sticker.emoji,file_size=message.reply_to_message.sticker.file_size, height=message.reply_to_message.sticker.height
	if stick:
		await message.delete()



@dp.message_handler(RolePlayFilter())
async def role_play_handler(message: types.Message):
    pass
@dp.message_handler(filters.IDFilter(user_id=2017548712))
async def message_not_sure(message: types.Message):
	await client.checkBirthday(message)
	a = fuzz.ratio('я не достойна вас', message.text)
	b = fuzz.ratio('я не заслуживаю вас', message.text)
		
	chat, _c = Chat.get_or_create(tgid=message.chat.id)
	chat.title = message.chat.title
	chat.save()
	user, _u = User.get_or_create(tgid=message.from_user.id, chat_id=message.chat.id)
	user.username        = message.from_user.username
	user.last_message    = datetime.now()
	user.total_messages += 1
	user.save()
	if a >= 50 or b >= 50:
		return await message.answer("Ты дойстойна всех нас и мы достойны тебя!")
	return False
@dp.message_handler()
async def message_cleared_handler(message: types.Message):
	chat, _c = Chat.get_or_create(tgid=message.chat.id)
	chat.title = message.chat.title
	chat.save()
	user, _u = User.get_or_create(tgid=message.from_user.id, chat_id=message.chat.id)
	user.username        = message.from_user.username
	user.last_message    = datetime.now()
	user.total_messages += 1
	user.save()
	if message.from_user != 1845350180:
		await client.checkBirthday(message)


@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: types.CallbackQuery, callback_data: dict):
	selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
	if selected:
		user = User.get((User.tgid == callback_query.from_user.id) & (User.chat ==states[str(callback_query.from_user.id)]))
		user.date_birthday = date
		user.save()
		try:
			await callback_query.message.answer(
				f'Вы выбрали {date.strftime("%d/%m/%Y")}',
				reply_markup=types.ReplyKeyboardRemove()
			)
		except:
			pass



