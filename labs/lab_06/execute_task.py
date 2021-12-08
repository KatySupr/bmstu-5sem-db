from tkinter import *
from tkinter import messagebox as mb


def create_list_box(rows, title, count=70):
    root = Tk()

    root.title(title)
    root.resizable(width=False, height=False)

    size = (count + 3) * len(rows[0]) + 1

    list_box = Listbox(root, width=size, height=15,
                       font="monospace 10", bg="lightsteelblue", highlightcolor='lightsteelblue', selectbackground='#59405c', fg="#59405c")

    list_box.insert(END, "█" * size)

    for row in rows:
        string = (("█ {:^" + str(count) + "} ") * len(row)).format(*row) + '█'
        list_box.insert(END, string)

    list_box.insert(END, "█" * size)

    list_box.grid(row=0, column=0)

    root.configure(bg="lightsteelblue")

    root.mainloop()


# Скалярный запрос
def execute_task1(cur, episodes):
    try:
        episodes = int(episodes.get())
    except:
        mb.showerror(title="Ошибка", message="Введите число!")
        return

    cur.execute(" \
        SELECT count(*) \
        FROM labs.anime \
        WHERE episodes= %s \
        GROUP BY episodes", (episodes,))

    row = cur.fetchone()

    mb.showinfo(title="Результат",
                message=f"Количество аниме с числом эпизодов = {episodes} составляет: {row[0]}")

# Запрос к метаданным
def execute_task4(cur, table_name, con):
    table_name = table_name.get()

    try:
        cur.execute(f"SELECT * FROM {table_name}")
    except:
        # Откатываемся.
        con.rollback()
        mb.showerror(title="Ошибка", message="Такой таблицы нет!")
        return

    rows = [(elem[0],) for elem in cur.description]

    create_list_box(rows, "Задание 4", 17)

# Многооператорная или табличнвя функция
def execute_task6(cur, episodes, mpaa):
    episodes = episodes.get()
    mpaa = str(mpaa.get())
    try:
        episodes = int(episodes)
    except:
        mb.showerror(title="Ошибка", message="Введите число!")
        return

    # getAnimesMult(int, text) - Многооператорная табличная функция
    # возвращает таблизу аниме с заданным числом эпизодов и определенного рейтинга
    cur.execute("select * from getAnimesMult(%s, %s)", (episodes, mpaa))

    rows = cur.fetchall()

    create_list_box(rows, "Задание 6", 30)

# хранимая процедура
def execute_task7(cur, param, con):
    try:
        a_id = int(param[0].get())
        new_rating = int(param[1].get())
    except:
        mb.showerror(title="Ошибка", message="Некорректные параметры!")
        return

    if new_rating < 0 or new_rating > 10:
        mb.showerror(title="Ошибка", message="Неподходящие значения!")
        return

    # Выполняем запрос.
    try:
        cur.execute("CALL updateViewedAnime(%s, %s);",
                    (a_id, new_rating))
    except:
        mb.showerror(title="Ошибка", message="Некорректный запрос!")
        # Откатываемся.
        con.rollback()
        return
        
    con.commit()

    mb.showinfo(title="Информация!", message="Оценка изменена!")

# Вставка данных в созданную таблицу с использованием инструкций insert и copy
def execute_task10(cur, param, con):
    try:
        user_id = int(param[0].get())
        reason = param[1].get()
    except:
        mb.showerror(title="Ошибка", message="Некорректные параметры!")
        return

    cur.execute(
        "select * from information_schema.tables where table_name='banned_users'")

    if not cur.fetchone():
        mb.showerror(title="Ошибка", message="Таблица не создана!")
        return

    try:
        cur.execute("insert into banned_users values(%s, %s)",
                    (user_id, reason))
    except:
        mb.showerror(title="Ошибка!", message="Ошибка запроса!")
        # Откатываемся.
        con.rollback()
        return

    # Фиксируем изменения.
    con.commit()

    mb.showinfo(title="Информация!", message="Еще один забанен!")