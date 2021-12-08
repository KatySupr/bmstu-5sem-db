-- 1 - предикат сравнения
-- аниме, количество эпизодов в котором меньше 13
select title, episodes
from labs.anime
where episodes < 13
order by episodes, title

-- 2 - предикат between
-- студии, в которых работает от 50 до 100 человек
select name, employees
from labs.studio s
where s.employees between 50 and 100

-- 3 предикат like
-- пользователи с почтой yandex
select nickname, email
from labs.users u
where u.email like '%@yandex.com%'
order by created_at

-- 4 - предикат in с вложенным подзапросом
-- никмеймы пользователей, которые ставили просмотренным аниме оценку выше 5
select nickname
from labs.users u
where u.id in (
	select id_user
	from labs.viewed_anime va
	where va.rating > 5
)

-- 5 - предикат exists с вложенным подзапросом
-- аниме, которым пользователь поставил оценку выше 7
select title, rating
from labs.anime a
where exists (
	select 1
	from labs.viewed_anime va
	where a.id = va.id_anime and va.rating > 7
)
order by rating

-- 6 - предикат сравнения с квантом
-- аниме, количество эпизодов в котором, больше какого-то количества эпизодов аниме, mpaa которого = 'NC-17', а рейтинг > 9
select title, episodes, mpaa
from labs.anime a1
where a1.episodes > any (
	select episodes
	from labs.anime a2
	where a2.mpaa = 'NC-17' and a2.rating > 9
)
order by rating

-- 7 - аггрегатные функции в выражениях столбцов
-- среднее число эпизодов в аниме
select avg(episodes) as ActualAVG, sum(episodes) / count(id) as CalcAVG
from labs.anime a

-- 8 - скалярные подзапросы в выражениях столбцов
-- аниме, полностью вышедшие до начала 2016 года, с учетом числа пользователей, их посмотревших
select title, (
	select count(id_user)
	from labs.viewed_anime va
	where va.id_anime = a.id
) as viewedCount
from labs.anime a
where a.end_at <= '2015-12-31'
order by title

-- 9 - простое выражение case
-- определение длинное/короткое аниме (по количеству эпизодов)
select title,
case
	 when episodes > 20 then 'длинное'
	 else 'короткое'
end as length
from labs.anime
order by title

-- 10 - поисковое выражение case
-- определение новая или старая крупная (более 100 работников) компания
select name, founded,
case
	when founded < '1970-12-31' then 'старая компания'
	else 'новая компания'
end as type
from labs.studio s
where employees > 1400
order by name

-- 11 - создание новой временной локальной таблицы из результирующего набора данных
-- пользователи, поставившие просмотренному аниме оценку быше 9
select u.nickname as nick
into usersAnime
from labs.users u join labs.viewed_anime va on va.id_anime = u.id
where va.rating > 9

select *
from usersAnime uA
order by nick

drop table usersAnime

-- 12 - вложенные коррелированные подзапросы в качестве производных таблиц в предложении from
-- студии и количество аниме, имми произведенное
select name, count
from (labs.anime a join (
	select studio_id as id, count(*)
	from labs.anime a1
	group by studio_id
) as a2 on a.studio_id = a2.id) as aa join labs.studio s on aa.studio_id = s.id
order by name

-- 13 - вложенные подзапросы с уровнем вложенности 3
-- аниме, созданные компаниями, в которых работают более 495 человек, которые были просмотрены пользователями
select title, nickname
from labs.anime a join labs.viewed_anime va on a.id = va.id_anime join labs.users u on va.id_user = u.id
where id_anime in (
	select id
	from labs.anime a
	group by id
	having studio_id in (
		select id
		from labs.studio s
		where employees > 495
	)
)

-- 14 - консолидирующая данные с помощью предложения group by, но без having
-- пользователи и количество просмотренных ими аниме
select nickname, count(id_anime) as viewed
from labs.viewed_anime va join labs.users u on va.id_user = u.id
group by nickname
order by viewed desc, nickname

-- 15 - консолидирующая данные с помощью предложения group by с having
-- пользователи, ставившие разные оценки просмотренным аниме
select nickname, avg(rating) as averageRating, min(rating) as minRating, max(rating) as maxRating
from labs.viewed_anime va join labs.users u on va.id_user = u.id
group by nickname
having max(rating) != min(rating)
order by nickname

-- 16 - insert вставка в таблицу одного значения
-- OLOLO в пользователи
insert into labs.users (nickname, created_at, country, email, sex)
values ('OLOLO', '1991-01-01', 'Germany', 'OLOLO@gmail.com', 'Male')

select *
from labs.users u
where u.nickname = 'OLOLO'

-- 17 - многострочная insert, вып. вставку в таблицу результирующего набора данных вложенного подзапроса
-- добавление в таблицу просмотренных аниме пользователей, зарегистрировавшихся после 2015 года, и аниме объемом от 12 до 22 эпизодов с минимальным id
insert into labs.viewed_anime (id_anime, id_user, start_at, end_at, rating)
select (
	select min(id)
	from labs.anime
	where episodes between 12 and 22
), id, '2020-01-01', '2020-01-05', 5
from labs.users
where created_at > '2015-01-01'

-- 18 - инструкция update
-- удвоить число сотрудников в студиях, зарегистрированных после 1980 года
update labs.studio
set employees = employees * 2
where founded >= '1980-01-01'

-- 19 - update со скалярным подзапросом в предложении set
-- установить максимальный рейтинг тех аниме, количество эпизодов в  котором не менее 500
update labs.anime
set rating = (
	select max(rating)
	from labs.anime
)
where episodes >= 500

-- 20 - delete
-- удалить из просмотренных те аниме, которым пользователи поставили оценку ниже 2
delete from labs.viewed_anime
where rating < 2

-- 21 - delete с вложенным коррелированным подзапросом в предложении where
-- удалить из просмотренных те аниме, количество эпизодов в которых меньше 5
delete from labs.viewed_anime
where id_user in (
	select id_user
	from labs.viewed_anime va join labs.anime a on va.id_anime = a.id
	where episodes < 5
)

-- 22 - простое обобщенное табличное выражение
with cn (rating, numOfAnime) as (
	select rating, count(*)
	from labs.viewed_anime
	group by rating
)
select *
from cn
order by rating

-- 23 - рекурсивное обобщенное табличное выражение
-- названия аниме, которые пользователи смотрели
with recursive num(id, title, rec) as (
	select id, title, null
	from labs.anime a 
	union all
	select num.id, num.title, '1'
	from labs.viewed_anime va join num on va.id_anime = num.id and rec is null
)
select title
from num
where rec is not null
order by id

-- 24 - оконные функции. использование min max avg over
select title, va.rating, avg(va.rating) over (partition by title) as averageRating
from labs.anime a join labs.viewed_anime va on a.id = va.id_anime
order by title

-- 25 - оконные функции для устранения дублей
update labs.viewed_anime
set id_anime = 13, start_at = '2021-01-01', end_at = '2021-02-01', rating = 5
where id_user between 1 and 10

update labs.viewed_anime
set id_user = 1
where id_anime = 13

delete from labs.viewed_anime
where id in(
	with tmp as(
		select id, id_anime, id_user, start_at, end_at, rating, row_number() over (partition by id_anime, id_user, start_at, end_at, rating) as n
		from labs.viewed_anime
	)
	select id
	from tmp
	where n > 1
)