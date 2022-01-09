from py_linq import *

from anime import *
from colors import *

def request_1(animes):
	# Аниме, число эпизодов в которых больше 50, отсортированные по названию
	result = animes.where(lambda x: x['episodes'] >= 12).order_by(lambda x: x['title']).select(lambda x: {x['title'], x['episodes']})
	return result

	# Отсортированные аниме
	# names = animes.select(lambda x: x['title']).order_by(lambda x: x)
	# names = animes.select(lambda x: {x['title'], x['episodes']})


def request_2(animes):
	# Необязательным параметром является условие. 
	# Количество аниме, которые были произведены студией с id 225
	result = animes.count(lambda x: x['studio_id'] == 225)
	
	return result


def request_3(animes):
	# минимальное и максимальное число эпизодов
	episodes = Enumerable([{animes.min(lambda x: x['episodes']), animes.max(lambda x: x['episodes'])}])
	# минимальный и максимальный рейтинг
	rating = Enumerable([{animes.min(lambda x: x['rating']), animes.max(lambda x: x['rating'])}])
	# А теперь объединяем все это.
	result = Enumerable(episodes).union(Enumerable(rating), lambda x: x)
	
	return result

def request_4(animes):
	# Группировка по жанру
	result = animes.group_by(key_names=['genre'], key=lambda x: x['genre']).select(lambda g: {'key': g.key.genre, 'count': g.count()})
	return result
	# Кол-во группировок.
	# tmp = animes.group_by(key_names=['genre'], key=lambda x: x['genre']).count()

def request_5(animes):
	pass
	device = Enumerable([{'id':595, 'slogan':'I want home'}, {'id':409, 'slogan':'Babochka'}, {'id':70, 'slogan':'Ebash'}])
	# inner_key = i_k первичный ключ
	# outer_key = o_k внешний ключ
	# inner join 
	s_d = animes.join(device, lambda o_k : o_k['studio_id'], lambda i_k: i_k['id'])

	return s_d

def task_1():
	# Создаем коллекцию.
	animes = Enumerable(create_animes('data/animes.csv'))

	print(GREEN, '\n1.Аниме, число эпизодов в которых больше 50, отсортированные по названию:\n')
	for elem in request_1(animes): 
		print(elem)

	print(YELLOW, f'\n2.Количество аниме, которые были произведены студией с id 225 =  {str(request_2(animes))}')

	print(BLUE, '\n3.Некоторые характеристики:\n')
	for elem in request_3(animes): 
		print(elem)

	print(GREEN, '\n4.Группировка по жанру:\n')
	for elem in request_4(animes): 
		print(elem)

	print(GREEN, '\n5.Соединяем аниме студию и лозунг:\n')
	for elem in request_5(animes): 
		print(elem)
