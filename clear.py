from peewee import Model, SqliteDatabase

# Подключение к базе данных
db = SqliteDatabase('database.db')

# Импорт модели из другого файла
from models.chat import User as _model

# Функция для очистки базы данных
def clear_database(model):
    # Удаление всех записей из модели
    model.delete().execute()

if __name__ == '__main__':
    # Очистка базы данных для вашей модели
    clear_database(_model)
