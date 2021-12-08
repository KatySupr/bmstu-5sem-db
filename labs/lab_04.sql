create extension plpython3u

-- Определяемая пользователем скалярная функция SQL CLR
-- возвращает email пользователя по id
create or replace function get_animes(id_ int)
returns text as $$
	usrs = plpy.execute('select * from users')
	for usr in usrs:
		if usr['id'] == id_:
			return usr['email']
	return None
$$ language plpython3u;

select * from get_animes(111);

-- Пользовательская агрегатная функция CLR
-- средняя оценка, просмотренных аниме
drop function avg_rating(a_id integer);

create or replace function avg_rating(a_id integer)
returns numeric as $$
	plan = plpy.prepare('select rating from viewed_anime where id_anime = $1', ["integer"])
	values = plpy.execute(plan, [a_id])
	
	sum = 0
	num = 0
	for v in values:
		sum += list(v.values())[0]
		num += 1
	
	return sum / num
$$ language plpython3u;

select id_anime, avg_rating(id_anime)
from labs.viewed_anime
group by id_anime
order by id_anime;
 
-- Определяемая пользователем табличная функция CLR
-- Вывести все аниме любимого пользователем жанра
drop function get_fav_anime(u_id integer)

create or replace function get_fav_anime(u_id integer)
returns table(title text, genre text, rating real) as $$
	res = []
	animes = plpy.execute('select title, genre, rating from anime')
	plan = plpy.prepare('select favorite_genre from users where id = $1', ['integer'])
	gen = plpy.execute(plan, [u_id])
	
	for elem in animes:
		if elem['genre'] == gen[0]['favorite_genre']:
			res.append(elem)
			
	return  res
$$ language plpython3u;

select *
from get_fav_anime(89)
order by rating desc 

-- Хранимая проецедура CLR
-- изменяют оценку просмотренного пользователем аниме
create or replace procedure updateRating(id_user integer, new_rating integer)
as $$
	plan = plpy.prepare('update viewed_anime set rating = $2 where id_user = $1', ['integer', 'integer'])
	plpy.execute(plan, [id_user, new_rating])
$$ language plpython3u

call updateRating(1, 9)

select id_user, rating
from viewed_anime
where id_user = 1

-- Триггер CLR
-- добавлять удаленных пользователей в отдельную таблицу
drop table deleted_people_audit

create table if not exists deleted_people_audit (
	id int not null primary key,
	nickname text not null,
	created_at timestamp not null,
	country text not null,
	email text not null,
	sex text
);

create or replace function backup_deleted_people()
returns trigger as $$
	plan = plpy.prepare('insert into deleted_people_audit(id, nickname, created_at, country, email, sex) values($1, $2, $3, $4, $5, $6);', ['int', 'text', 'timestamp', 'text', 'text', 'text'])
	pi = TD['old']
	rv = plpy.execute(plan, [pi['id'], pi['nickname'], pi['created_at'], pi['country'], pi['email'], pi['sex']])
	return TD['new']
$$ language plpython3u;

create trigger backup_deleted_people
before delete on users for each row 
execute  procedure backup_deleted_people();

delete from users 
where id = 1001

select * from deleted_people_audit 

-- Определяемый пользователем тип данных CLR
-- Получение краткой информации об аниме
create type animeRating as (
	title text,
	rating real
);

create or replace function get_short_anime_info(a_id int)
returns animeRating as $$
	plan = plpy.prepare('select title, rating from anime where id = $1', ['integer'])
	dt = plpy.execute(plan, [a_id])
	
	return (dt[0]['title'], dt[0]['rating'])
$$ language plpython3u;

select *
from get_short_anime_info(1)




