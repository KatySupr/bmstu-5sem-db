import collections
import datetime
from peewee import *

from colors import *

from datetime import datetime

# Подключаемся к нашей БД.
con = PostgresqlDatabase(
	database="Anime",
    user="postgres",
    password="postgres",
    host="127.0.0.1",  # Адрес сервера базы данных.
    port="5432",	   # Номер порта
    options="-c search_path=labs"
)


class BaseModel(Model):
	class Meta:
		database = con

class Anime(BaseModel):
	id = IntegerField(column_name='id')
	title = CharField(column_name='title')
	studio_id = IntegerField(column_name='studio_id')
	episodes = IntegerField(column_name='episodes')
	mpaa = CharField(column_name='mpaa')
	start_at = DateField(column_name='start_at')
	end_at = DateField(column_name='end_at')
	rating = FloatField(column_name='rating')

	class Meta:
		table_name = 'anime'

class User(BaseModel):
	id = IntegerField(column_name='id')
	nickname = CharField(column_name='nickname')
	created_at = DateTimeField(column_name='created_at')
	country = CharField(column_name='country')
	email = CharField(column_name='email')
	sex = CharField(column_name='sex')

	class Meta:
		table_name = 'users'

class Viewed_anime(BaseModel):
	id = IntegerField(column_name='id')
	id_anime = IntegerField(column_name='id_anime')
	id_user = IntegerField(column_name='id_user')
	start_at = DateTimeField(column_name='start_at')
	end_at = DateTimeField(column_name='end_at')
	rating = IntegerField(column_name='rating')

	class Meta:
		table_name = 'viewed_anime'

def query_1():
	# 1. Однотабличный запрос на выборку.
	anime = Anime.get(Anime.id == 2)
	print(GREEN, f'{"1. Однотабличный запрос на выборку:":^130}')
	print(anime.id, anime.title, anime.episodes, anime.mpaa, anime.rating)
	

	# Получаем набор записей.
	query = Anime.select().where(Anime.episodes > 18).limit(5).order_by(Anime.id)

	print(BLUE, f'\n{"Запрос:":^130}\n\n', query, '\n')
	
	animes_selected = query.dicts().execute()

	print(YELLOW, f'\n{"Результат:":^130}\n')
	for elem in animes_selected:
		print(elem)

def query_2():
	# 2. Многотабличный запрос на выборку.
	global con 
	print(GREEN, f'\n{"2. Многотабличный запрос на выборку:":^130}\n')
	
	print(BLUE, f'{"Аниме и просмотревшие их пользователи:":^130}\n')

	# Аниме, которые просмотрели пользователи
	query = Anime.select(Anime.id, Anime.title, Anime.rating).join(Viewed_anime, on=(Anime.id == Viewed_anime.id_anime)).order_by(Anime.id).limit(5)
	
	a_b = query.dicts().execute()
	for elem in a_b:
		print(elem)

	print(GREEN, f'\n{"Пользователи и аниме, которые они посмотрели:":^130}\n')

	# Пользователи и аниме, которые они посмотрели.
	query = User.select(User.nickname, Anime.title).join(Viewed_anime, on=(User.id == Viewed_anime.id_user)).join(Anime, on=(Viewed_anime.id_anime == Anime.id)).limit(5)

	u_d = query.dicts().execute()

	for elem in u_d:
		print(elem)

def print_last_five_users():
	# Вывод последних 5-ти записей.
	print(BLUE, f'\n{"Последние 5 пользователей:":^130}\n')
	query = User.select().limit(5).order_by(User.id.desc())
	for elem in query.dicts().execute():
		print(elem)
	print()

def add_user(new_id, new_nickname, new_created_at, new_country, new_email, new_sex):
	global con 
	
	try:
			with con.atomic() as txn:
				# user = User.get(User.id == new_id)
				User.create(id = new_id, nickname=new_nickname, created_at=new_created_at, country=new_country, email=new_email, sex=new_sex)
				print(GREEN, "Пользователь успешно добавлен!")
	except:
			print(YELLOW, "Пользователь уже существует!")
			txn.rollback()

def update_nickname(user_id, new_nickname):
	user = User(id=user_id)
	user.nickname = new_nickname
	user.save()	
	print(GREEN, "Nickname успешно обновлен!")

def del_user(user_id):
	user = User.get(User.id == user_id)
	user.delete_instance()
	print(GREEN, "Пользователь успешно удален удален!")

def query_3():
	# 3. Три запроса на добавление, изменение и удаление данных в базе данных.
	print(GREEN, f'\n{"3. Три запроса на добавление, изменение и удаление данных в базе данных:":^130}\n')

	print_last_five_users()
	add_user(1001, 'Katusha', datetime.now(), 'Russia', 'katy@yandex.com', 'Female')
	print_last_five_users()

	update_nickname(1001, 'Katy')
	print_last_five_users()

	del_user(1001)	
	print_last_five_users()

def query_4():
	# 4. Получение доступа к данным, выполняя только хранимую процедуру.
	global con 
	# Можно выполнять простые запросы.
	cursor = con.cursor()

	print(GREEN, f'\n{"4. Получение доступа к данным, выполняя только хранимую процедуру:":^130}\n')

	cursor.execute("CALL updateViewedAnime(%s, %s);", (157,5))
	# # Фиксируем изменения.
	# # Т.е. посылаем команду в бд.
	# # Метод commit() помогает нам применить изменения,
	# # которые мы внесли в базу данных,
	# # и эти изменения не могут быть отменены,
	# # если commit() выполнится успешно.
	con.commit()

	print(GREEN, f'Рейтинг просметренного аниме (id_anime = {157}) успешно изменено на {5}.\n')

	cursor.execute("CALL updateViewedAnime(%s, %s);", (157,7))
	con.commit()

	cursor.close()
	


def task_3():
	global con 

	query_1()
	query_2()
	query_3()
	query_4()

	con.close()	