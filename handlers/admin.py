import asyncio

import loguru
from bot import bot
from aiogram import types, filters
from models.chat import AdWord, BanStick, RolePlay, User, Chat, Week, Warn
from state import RolePlayAdd
from aiogram.fsm.context import FSMContext
from texts import admin as text
import schedule
from datetime import datetime
from aiogram import Router
from midllwares import CounterMiddleware
router = Router()
router.message.middleware(CounterMiddleware())

@router.message(filters.Command('gprofile'))
async def gprofile_handler(message: types.Message):
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	if chat_member.can_delete_messages:
		users = User.select().where(User.chat == message.chat.id)
		total_messages = 0
		acivity_users = 0
		members = await bot.get_chat_member_count(message.chat.id)
		for user in users:
			if user.total_messages >= 1200:
				acivity_users += 1
			total_messages += user.total_messages	
		return await message.answer(text.GPROFILE.format(
			chattitle=message.chat.title,
			activity_members=acivity_users,
			total_messages=total_messages,
			members=members
			))


@router.message(filters.Command('db'))
@router.message(filters.Command('db'))
@router.message(filters.Command('db'))
async def db(message: types.Message):
	if message.chat.type.lower() not in ['group', 'supergroup']: return None
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	if chat_member.can_delete_messages:
		inkbs = types.InlineKeyboardMarkup()

		users = User.select().where(User.chat == message.chat.id).limit(10)
		loguru.logger.info(len(users))
		loguru.logger.info(message.chat.id)
		for user in users:
			inkbs.add(types.InlineKeyboardButton(f'{user.username}', callback_data=f'getDB={user.id}'))
		inkbs.add(types.InlineKeyboardButton(f'Назад', callback_data=f'getDBBACK=0={message.chat.id}'),types.InlineKeyboardButton(f'Вперед', callback_data=f'getDBBACK=1={message.chat.id}'))
		await message.bot.send_message(chat_id=message.from_user.id,text='db', reply_markup=inkbs)


@router.message(filters.Command('warns'))
@router.message(filters.Command('warns'))
async def warns(message: types.Message):
	if message.chat.type.lower() not in ['group', 'supergroup']: return None
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	if chat_member.can_delete_messages:
		user = User.get((User.tgid == message.reply_to_message.from_user.id) & (User.chat == message.chat.id))
		warns = Warn.select().where(Warn.user == user)
		warns_ = ''
		for warn in warns:
			warns_ += f'Предупреждение по правилу {warn.rule}\n'
		if warns != '':
			await message.answer(warns_)
		else:
			await message.answer('Варнов не обнаружено.')
	else:
		await message.answer("Вы не админ")


@router.message(filters.Command('warn'))
@router.message(filters.Command('warn'))
async def warn(message: types.Message):
	if message.chat.type.lower() not in ['group', 'supergroup']: return None
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	if chat_member.can_delete_messages and ' ' in message.text and message.reply_to_message:
		rule = int(message.text.split(' ')[1])
		user = User.get((User.tgid == message.reply_to_message.from_user.id) & (User.chat == message.chat.id))
		if message.reply_to_message.text:
			warn = Warn.create(user=user, rule=rule,message=message.reply_to_message.text)
		elif message.reply_to_message.caption:
			warn = Warn.create(user=user, rule=rule,message=message.reply_to_message.text)
		else:
			warn = Warn.create(user=user, rule=rule,message="None")
		warn.save()
		warns = Warn.select().where(Warn.user == user.id).count()
		await message.reply(f"Пользователю @{message.reply_to_message.from_user.username} выдано предупреждение. Причина: правило {rule} \nУже варнов: {warns}")
	elif message.reply_to_message: # ???
		await message.reply(text.NOT_REPLY)
	else:
		await message.reply(text.NOT_RULE)

@router.message(filters.Command('del'))
async def delmsgs(message: types.Message):
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	if chat_member.can_delete_messages:
		await message.reply_to_message.delete()
		await message.delete()



@router.message(filters.Command('send'))
async def ban_stick_handler(message: types.Message):
	if message.from_user.id != 848150113: return None
	await bot.send_message(-1001786418282, message.text.replace('/send ', ''))

@router.message(filters.Command('clear'))
async def clear_handler(message: types.Message):
	if message.from_user.id != 848150113: return None
	users = User.select() 
	weekNumber = datetime.now().isocalendar()[1]
	for user in users:
		week, _ = Week.get_or_create(weekNumber=int(weekNumber), user=user.id, total_messages=user.total_messages)
		week.save()
		user.total_messages = 0
		user.save()


@router.message( filters.Command('cuser'))
async def inactive_top(message: types.Message, state: FSMContext):
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	cmd = message.text.replace('/cuser', '')
	cmdX = cmd.split(' ')
	if len(cmdX) != 0:
		if chat_member.can_delete_messages:
			user = User.get(User.username == message.text.replace('/cuser ', '').replace('@',''))
			chat_member = await message.bot.get_chat_member(chat_id, user.tgid)
			ruser = state.current_state(user=user.tgid, chat=message.chat.id)
			ruser_ = await ruser.get_data('ruser')
			user_state = state.current_state(user=ruser_['ruser'][0], chat=message.chat.id)
			await ruser.finish()
			await user_state.finish()
			_ruser = await message.bot.get_chat_member(chat_id, int(ruser_['ruser'][0]))
			await message.reply(f'Теперь @{user.username} и @{_ruser.user.username} могут заново выбрать пользователя')
		else:
			await message.reply('Админ комманда')
	else:
		await message.reply('Укажите юзернейм')

@router.message( filters.Command('ban_stick'))
async def ban_stick_handler(message: types.Message):
	user_id = message.from_user.id
	chat_id = message.chat.id
	chat_member = await message.bot.get_chat_member(chat_id, user_id)
	if chat_member.can_delete_messages:
		if message.reply_to_message and message.reply_to_message.content_type == "sticker":
			banstick, _ = BanStick.get_or_create(emoji=message.reply_to_message.sticker.emoji,file_size=message.reply_to_message.sticker.file_size, height=message.reply_to_message.sticker.height, chat=message.chat.id)
			
			if _:
				banstick.save()
				await message.answer(text.ADMIN_BAN_STICK_SUCCESS)
				await message.reply_to_message.delete()
				await message.delete()
			else:
				await message.answer(text.ADMIN_BAN_STICK_NOT_SUCCESS)
		else:
			await message.answer(text.NEED_STICK)

@router.message(filters.Command('rp_add'))
async def ban_stick_handler(message: types.Message, state: FSMContext):
	if message.chat.type.lower() not in ['private']: return None

	if message.from_user.id == 848150113:
		await message.answer('Введите комманду')
		await state.set_state(RolePlayAdd.cmd)


@router.message(RolePlayAdd.cmd)
async def ban_stick_handler(message: types.Message, state: FSMContext):
	if message.chat.type.lower() not in ['private']: return None
	await state.update_data(cmd = message.text)
	await message.answer('Введите общий текст')
	await state.set_state(RolePlayAdd.text)

@router.message( RolePlayAdd.text)
async def ban_stick_handler(message: types.Message, state: FSMContext):
	if message.chat.type.lower() not in ['private']: return None
	await state.update_data(text = message.text)
	await message.answer('Введите одиночный текст')
	await state.set_state(RolePlayAdd.textself)


@router.message( RolePlayAdd.textself)
async def ban_stick_handler(message: types.Message, state: FSMContext):
	if message.chat.type.lower() not in ['private']: return None
	data = await state.get_data()
	rp = RolePlay.create(cmd=data['cmd'], text=data['text'], textself=message.text)
	rp.save()
	await message.answer('Команда успешно добавлена')
	await state.clear()

"""
@dp.callback_query_handler(filters.Text(startswith="getDBBACK="), state="*")
async def getDB(callback: types.callback_query):
	offset, chatid = callback.data.replace('getDBBACK=', '').split('=')
	offset = int(offset)
	inkbs = types.InlineKeyboardMarkup()
	if offset <= 0:
		return None
	users = User.select().where(User.chat == chatid).offset(int(offset*10)).limit(10)
	for user in users:
		inkbs.add(types.InlineKeyboardButton(f'{user.username}', callback_data=f'getDB={user.id}'))
	inkbs.add(types.InlineKeyboardButton(f'Назад', callback_data=f'getDBBACK={offset-1}={chatid}'),types.InlineKeyboardButton(f'Вперед', callback_data=f'getDBBACK={offset+1}={chatid}'))
	# await callback.message.edit_reply_markup(inkbs)
	await callback.message.answer(text='db', reply_markup=inkbs)
	await callback.message.delete()

@dp.callback_query_handler(filters.Text(startswith="getDBBACK="), state="*")
async def getDB(callback: types.callback_query):
	offset, chatid = callback.data.replace('getDBBACK=', '').split('=')
	offset = int(offset)
	inkbs = types.InlineKeyboardMarkup()
	if offset <= 0:
		return None
	users = User.select().where(User.chat == chatid).limit(10).offset(int(offset*10))
	if len(users) == 0:
		return None
	for user in users:
		inkbs.add(types.InlineKeyboardButton(f'{user.username}', callback_data=f'getDB={user.id}'))
	inkbs.add(types.InlineKeyboardButton(f'Назад', callback_data=f'getDBBACK={offset-1}={chatid}'),types.InlineKeyboardButton(f'Вперед', callback_data=f'getDBBACK={offset+1}={chatid}'))
	# await callback.message.edit_reply_markup(inkbs)	
	await callback.message.answer(text='db', reply_markup=inkbs)
	await callback.message.delete()
# @dp.callback_query_handler(filters.Text(startswith="kom_vote_check_"), state="*")
# async def kom_vote_check(cb: types.callback_query):

@dp.callback_query_handler(filters.Text(startswith="getDB="), state="*")
async def getDB(callback: types.callback_query):
	data = int(callback.data.replace('getDB=', ''))
	user = User.get_by_id(data)
	weeks = Week.select().where(Week.user == user.id)
	warns = Warn.select().where(Warn.user == user.id)
	total_messages = user.total_messages
	warns_ = ''
	for week in weeks:
		total_messages += week.total_messages
	for warn in warns:
		warns_ += f'Предупреждение по правилу {warn.rule}\n'
	await callback.message.answer(text.DB_USER.format(username=user.username, total_messages=total_messages, date_of_birdth=user.date_birthday, warns=warns, message_date=user.last_message))

"""