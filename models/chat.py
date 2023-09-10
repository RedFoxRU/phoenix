from datetime import datetime
from peewee import *
from config import DBNAME, PWD
from playhouse.migrate import *

db = SqliteDatabase(PWD+DBNAME)

class Chat (Model):
    id = PrimaryKeyField()
    tgid = IntegerField()
    members = IntegerField(default=2)
    title = CharField(null=True)
    adMessagesDelete = IntegerField(default=0)
    
    class Meta:
        database = db
        
class RolePlay (Model):
    id = PrimaryKeyField()
    cmd = CharField(unique=True)
    text = TextField()
    textself = TextField()
    
    class Meta:
        database = db
        
class User(Model):
    id = PrimaryKeyField()
    tgid = IntegerField()
    username = CharField(null=True)
    chat = ForeignKeyField(Chat, 'tgid')
    last_message = DateTimeField(null=True)
    total_messages = IntegerField(default=0)
    warns = IntegerField(default=0)
    date_birthday = DateField(null=True)
    # addDate = DateField(null=True)
    hobby = TextField(null=True)
    country = CharField(null=True)
    city = CharField(null=True)
    confidentiality = IntegerField(default=0)
    beverage = CharField(null=True) # Напитки
    
    class Meta:
        database = db

class Week(Model):
    id = PrimaryKeyField()
    weekNumber = IntegerField()
    user = ForeignKeyField(User, "id")
    total_messages = IntegerField()

    class Meta:
        database=db

class Warn(Model):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, "id")
    rule = IntegerField()
    message = TextField()

    class Meta:
        database=db

class AdWord(Model):
    id = PrimaryKeyField()
    word = CharField()
    
    class Meta:
        database=db

class Message(Model):
    user = ForeignKeyField(User, User.id)
    text = TextField()
    
    class Meta:
        database = db

class BanStick(Model):
    id = PrimaryKeyField()
    emoji = CharField()
    file_size = IntegerField()
    height = IntegerField()
    chat = ForeignKeyField(Chat, 'tgid')
    
    class Meta:
        database = db
        
Chat.create_table()
RolePlay.create_table()
User.create_table()
Week.create_table()
Warn.create_table()
AdWord.create_table()
Message.create_table()
BanStick.create_table()




def my_migrate():
    migrator = SqliteMigrator(db)

    with db.atomic():
        migrate(     
            migrator.add_column('User', 'addDate', DateField(default=datetime.now())),
        )


# if __name__ == "__main__":
# my_migrate()