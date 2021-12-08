from tk import *

import psycopg2


def main():
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
        return

    print("База данных успешно открыта")

    # Объект cursor используется для фактического
    # выполнения наших команд.
    cur = con.cursor()

    # Интерфейс.
    window(cur, con)

    # Закрываем соединение с БД.
    cur.close()
    con.close()


if __name__ == "__main__":
    main()





# 11 --- Аниме ккакой студии больше всего просматриваются
# Название студии, число пользователей, просмотревших аниме этой студии
# Распечатать в json формате