from datetime import datetime
import schedule
import time
from models.chat import User, Week

def clr_and_take_to_week():
    users = User.select() 
    for user in users:
        week, _ = Week.get_or_create(weekNumber=datetime.now().isocalendar()[1], user=user.id,total_messages=user.total_messages)
        week.save()
        user.total_messages = 0
        user.save()

schedule.every().monday.at('23:58:59').do(clr_and_take_to_week)
while True:
    schedule.run_pending()
    time.sleep(1)