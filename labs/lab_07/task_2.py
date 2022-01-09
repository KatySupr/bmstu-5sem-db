from anime import *
import json
import psycopg2

from colors import * 

def connection():
	con = None
	# Подключаемся к БД.
	try:
		con = psycopg2.connect(
            database="Anime",
            user="postgres",
            password="postgres",
            host="127.0.0.1",  # Адрес сервера базы данных.
            port="5432",	   # Номер порта
            options="-c search_path=labs"
		)
	except:
		print("Ошибка при подключении к БД")
		return con

	print("База данных успешно открыта")
	return con
	
def output_json(array):
	print(BLUE)
	for elem in array:
		print(json.dumps(elem.get(), ensure_ascii=False))
	print(YELLOW)

def read_table_json(cur, count = 15):
	# Возвращает массив кортежей словарей.
	cur.execute("select * from animes_json")

	# with open('data/task_2.json', 'w') as f:
	    # f.write(rows)

	rows = cur.fetchmany(count)

	array = list()
	for elem in rows: 
		tmp = elem[0]
		# print(elem[0], sep=' ', end='\n')
		array.append(anime(tmp['id'], tmp['title'], tmp['studio_id'], tmp['episodes'],
		tmp['mpaa'], tmp['start_at'], tmp['end_at'], tmp['rating'], tmp['genre']))

	print(GREEN,f"id title studio_id episodes mpaa start_at end_at rating genre")
	print(*array, sep='\n')
	
	return array


def update_anime(animes, in_id):
	# Уменьшает рейтинг аниме
	for elem in animes:
		if elem.id == in_id:
			elem.rating -= 1
			if elem.rating <= 0:
				elem.rating = 0

	# dumps - сериализация. 
	# print(json.dumps(animes[0].get()))
	output_json(animes)

def add_anime(animes, anime):
	animes.append(anime)
	output_json(animes)

def task_2():
	con = connection()
	# Объект cursor используется для фактического
	# выполнения наших команд.
	cur = con.cursor()

	# 1. Чтение из XML/JSON документа.
	print(GREEN, f'{"1.Чтение из XML/JSON документа:":^130}')
	animes_array = read_table_json(cur)
	# 2. Обновление XML/JSON документа.
	print(BLUE, f'\n{"1.Обновление XML/JSON документа:":^130}')
	update_anime(animes_array, 2)
	# 3. Запись (Добавление) в XML/JSON документ.
	print(BLUE, f'{"1.Запись (Добавление) в XML/JSON документ:":^130}')
	add_anime(animes_array, anime(1277, 'OLOLO', 20, 24, 'R', '1993-04-13', '1999-07-05', 7.4, 'Комодо'))

	# Закрываем соединение с БД.
	cur.close()
	con.close()