from execute_task import *

# Скалярный запрос
def task1(cur, con = None):
    root_1 = Tk()

    root_1.title('Задание 1')
    root_1.geometry("300x200")
    root_1.configure(bg="lightsteelblue")
    root_1.resizable(width=False, height=False)

    Label(root_1, text="  Введите число эпизодов:", bg="lightsteelblue").place(
        x=75, y=50)
    episodes = Entry(root_1)
    episodes.place(x=75, y=85, width=150)

    b = Button(root_1, text="Выполнить",
               command=lambda arg1=cur, arg2=episodes: execute_task1(arg1, arg2),  bg="cornflowerblue")
    b.place(x=75, y=120, width=150)

    root_1.mainloop()

# Запрос с несколькими соединениями (join)
def task2(cur, con = None):
    cur.execute(" select title, name as studio_name \
                  from labs.anime a join labs.studio s on a.studio_id = s.id;")

    rows = cur.fetchall()
    # print(rows)

    create_list_box(rows, "Задание 2")


def task3(cur, con = None):
    # Добавить столбец с суммой кол-ва часов по группам возраста.
    cur.execute("with cn (rating, numOfAnime) as ( \
                    select rating, count(*) \
                    from labs.viewed_anime \
                    group by rating ) \
                select * \
                from cn \
                order by rating")

    rows = cur.fetchall()
    create_list_box(rows, "Задание 3")

# Запрос к метаданным
# Есть ли таблица
def task4(cur, con):

    root_1 = Tk()

    root_1.title('Задание 4')
    root_1.geometry("300x200")
    root_1.configure(bg="lightsteelblue")
    root_1.resizable(width=False, height=False)

    Label(root_1, text="Введите название таблицы:", bg="lightsteelblue").place(
        x=65, y=50)
    name = Entry(root_1)
    name.place(x=75, y=85, width=150)

    b = Button(root_1, text="Выполнить",
               command=lambda arg1=cur, arg2=name: execute_task4(arg1, arg2, con),  bg="cornflowerblue")
    b.place(x=75, y=120, width=150)

    root_1.mainloop()

# Вызов скалярной функции
#  ----Доделать-----
def task5(cur, con = None):
    cur.execute("select avg(rating) from labs.viewed_anime;")

    row = cur.fetchone()

    mb.showinfo(title="Результат",
                message=f"Средний рейтинг составляет: {row[0]}")


# Вызов многоператорной иили табличной функции
def task6(cur, con = None):
    root = Tk()

    root.title('Задание 6')
    root.geometry("300x200")
    root.configure(bg="lightsteelblue")
    root.resizable(width=False, height=False)

    Label(root, text="  Введите число эпизодов:", bg="lightsteelblue").place(
        x=10, y=50)
    episodes = Entry(root)
    episodes.place(x=200, y=50, width=80)
    Label(root, text="  Введите mpaa:", bg="lightsteelblue").place(
        x=10, y=100)
    mpaa = Entry(root)
    mpaa.place(x=150, y=100, width=100)

    b = Button(root, text="Выполнить",
               command=lambda arg1=cur, arg2=episodes, arg3=mpaa: execute_task6(arg1, arg2, arg3),  bg="cornflowerblue")
    b.place(x=75, y=140, width=150)

    root.mainloop()


def task7(cur, con=None):
    root = Tk()

    root.title('Задание 7')
    root.geometry("350x200")
    root.configure(bg="lightsteelblue")
    root.resizable(width=False, height=False)

    Label(root, text="  Введите id аниме:", bg="lightsteelblue").place(
        x=10, y=50)
    a_id = Entry(root)
    a_id.place(x=200, y=50, width=80)
    Label(root, text="  Введите новую оценку:", bg="lightsteelblue").place(
        x=10, y=100)
    new_r = Entry(root)
    new_r.place(x=200, y=100, width=100)

    param = [a_id, new_r]

    b = Button(root, text="Выполнить",
               command=lambda: execute_task7(cur, param, con),  bg="cornflowerblue")
    b.place(x=70, y=140, width=150)

    root.mainloop()

# Вызов системной функции или процедуры
def task8(cur, con = None):
    # Информация:
    # https://postgrespro.ru/docs/postgrespro/10/functions-info
    cur.execute(
        "SELECT current_database(), current_user;")
    current_database, current_user = cur.fetchone()
    mb.showinfo(title="Информация",
                message=f"Имя текущей базы данных:\n{current_database}\nИмя пользователя:\n{current_user}")


# Создание таблицы
def task9(cur, con):
    cur.execute(" \
        create table if not exists labs.banned_users \
        ( \
            id_user INT, \
            FOREIGN KEY(id_user) REFERENCES labs.users(id), \
            reason text \
        ) ")

    con.commit()

    mb.showinfo(title="Информация",
                message="Таблица успешно создана!")


def task10(cur, con):
    root = Tk()

    root.title('Задание 10')
    root.geometry("400x300")
    root.configure(bg="lightsteelblue")
    root.resizable(width=False, height=False)

    names = ["идентификатор человека",
             "причину"]

    param = list()

    i = 0
    for elem in names:
        Label(root, text=f"Введите {elem}:",
              bg="lightsteelblue").place(x=70, y=i + 25)
        elem = Entry(root)
        i += 50
        elem.place(x=115, y=i, width=150)
        param.append(elem)

    b = Button(root, text="Выполнить",
               command=lambda: execute_task10(cur, param, con),  bg="cornflowerblue")
    b.place(x=115, y=200, width=150)

    root.mainloop()

def task11(cur, con):
    print('Защита')

    cur.execute("select * from most_popular_studio()")

    row = cur.fetchone()

    mb.showinfo(title="Результат",
                message=f"id студии: {row[0]}\n\n\
Название студии: {row[1]}\n\n\
Число зрителей их аниме: {row[2]}")