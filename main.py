import asyncio
from datetime import datetime
import os
from random import randint
from texts import client as texts
from bot import dp, bot, set_commands
from config import PWD,DBNAME
import handlers
from models.chat import User, Week
import aioschedule
from loguru import logger
import database
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def clear ():
	users = User.select() 
	logger.info('clear')
	weekNumber = datetime.now().isocalendar()[1]
	for user in users:
		week, _ = Week.get_or_create(weekNumber=int(weekNumber), user=user.id, total_messages=user.total_messages)
		week.save()
		user.total_messages = 0
		user.save()

async def happyBearthday():
	# database.main(PWD+DBNAME)
	logger.info('happyBearthday')
	users = User.select() 
	now = datetime.now()
	for user in users:
		if user.date_birthday and now.month == user.date_birthday.month and now.day == user.date_birthday.day:
			try:
				await bot.send_message(user.chat.tgid, texts.HAPPY_BEARTHDAY_CHAT[randint(0,len(texts.HAPPY_BEARTHDAY_CHAT)-1)].format(username=user.username))
			except Exception as er:
				logger.debug(er)
			try:
				await bot.send_message(user.tgid, texts.HAPPY_BEARTHDAY_PC[randint(0,len(texts.HAPPY_BEARTHDAY_PC)-1)])
			except:
				pass

async def scheduler():
    aioschedule.every().monday.at('00:00').do(clear)
    aioschedule.every().day.at('8:00').do(happyBearthday)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(dp): 
	await set_commands()
	asyncio.create_task(scheduler())

async def main():
	scheduler = AsyncIOScheduler()

	scheduler.add_job(clear,'cron',day_of_week='mon',hour=00, minute=00)
	scheduler.start()
	dp.include_routers(handlers.admin.router,handlers.roleplay.router,
                    handlers.client.router, handlers.inline_mode.router)
	await dp.start_polling(bot, on_startup=on_startup)


if __name__ == '__main__':
    asyncio.run(main())
