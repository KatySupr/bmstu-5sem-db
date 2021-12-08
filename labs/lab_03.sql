-- 1 - Скалярная функция
-- найти средний рейтинг аниме, количество эпизодов в которых между ep1 и ep2
create function avgAnimeRating(int, int)
returns real as
$$
declare
	avgRating real;
begin
	select avg(rating) 
	from anime into avgRating 
	where episodes >= $1 and episodes <=$2;
	return avgRating;
end
$$
language plpgsql;

select avgAnimeRating(1, 20);

-- 2 - Посдставляемая табличная функция
-- возвращает (название аниме; название студии; никнейм пользователя, просмотервшего аниме)
create or replace function getAnimes() 
returns table(anime text, studio text, nickname text) as
$$
begin
		return query select a.title, s."name", u.nickname
		from anime a join studio s on a.studio_id = s.id
		join viewed_anime va on a.id = va.id_anime 
		join users u on va.id_user = u.id;
end
$$ language plpgsql

select *
from getAnimes()
order by anime;

-- 3 - Многооператорная табличная функция
-- возвращает таблизу аниме с заданным числом эпизодов и определенного рейтинга
create or replace function getAnimesMult(int, text)
returns table
(
	id int,
	title text,
	episodes int,
	mpaa text,
	genre text
)
as $$
	select id, title, episodes, mpaa, genre
	from anime
	where episodes = $1 and mpaa = $2;
$$ language sql;

select *
from getanimesmult(12, 'NC-17')

-- 4 - Рекурсивная функция или функция с рекурсивным ОТВ
--create or replace function st_friend(uid int, lf int)
--returns int as 
--$$
--declare 
--	res int;
--begin
--	select st_friend(id_friend, id_friend)
--	from labs.users into res
--	where id = uid and id_friend is not null;
--	if res is null then
--		return lf;
--	else
--		return res;
--	end if;
--end
--$$ language plpgsql
--
--select id as user_id, st_friend(id, id_friend) as far_friend
--from labs.users
--where id_friend is not null

create or replace function recFunc ()
returns table (id int, id_parent int, name text, level int)
language sql as $$
   with recursive r as (
   select id, id_parent, name, 1 as level 
   from geo 
   where id = 4
   union all
   select geo.id, geo.id_parent, geo.name, r.level + 1 as level 
   from geo join r on geo.id_parent = r.id
) select * from r;
$$;

select *
from recFunc();

-- 5 - Хранимая процедура без параметров или с параметрами
create or replace procedure updateViewedAnime(i int, r int)
as $$
begin 
	update viewed_anime
	set rating = r
	where id_anime = i;
end
$$ language plpgsql

call updateViewedAnime(152, 7)

select *
from labs.viewed_anime va
where id_anime = 152

-- 6 - Рекурсивная хранимая процедура или хранимая процедура с рекурсивным ОТВ
create or replace procedure prec() as 
$$
	with recursive r as (
		select id, id_parent, name, 1 as level
		from geo
		where id = 4
		union all
		select geo.id, geo.id_parent, geo.name, r.level + 1 as level
		from geo join r on geo.id_parent = r.id
	) select * from r;
$$ language sql;

call prec()

-- 7 - Хранимая процедура с курсором
select *
into temp users_copy 
from users

drop table users_copy

create or replace procedure fcurs(old_gen text, new_gen text) as 
$$
declare cur cursor for select * from users_copy where favorite_genre = old_gen;
		row record;
begin
	open cur;
	loop
		fetch cur into row;
		exit when not found;
		update users_copy
		set favorite_genre = new_gen
		where users_copy.id = row.id;
	end loop;
	close cur;
end
$$ language plpgsql;

call fcurs('Дзёсэй', 'Сёнэн')

select u.id, u.nickname, u.favorite_genre as old_fav_genre, uc.favorite_genre as new_fav_genre
from users u join users_copy uc on u.id = uc.id
where u.favorite_genre = 'Дзёсэй'

-- 8 - Хранимая процедура доступа к метаданным
-- кол-во ключей в таблицах (первичных и внешних)
create procedure count_key_column() as 
$$
declare 
	res int;
begin
	select count(*) into res 
	from information_schema.key_column_usage;
	raise notice 'Count of key columns usages %', res;
end
$$ language plpgsql

call count_key_column()

select *
from information_schema.key_column_usage kcu 

-- 9 - Триггер AFTER
create table if not exists rating_changes_audit
(
	change_id int not null,
	change_date text not null
);

create or replace function log_func()
returns trigger as 
$example_table$
begin
	insert into rating_changes_audit(change_id, change_date) values (new.id, current_timestamp);
	return new;
end
$example_table$ language plpgsql

create trigger new_rating
after update of rating on viewed_anime
for each row
execute procedure  log_func();

update labs.viewed_anime 
set rating = 9
where id = 1

select *
from rating_changes_audit 

-- 10 -Триггер INSTED OF
create view users_view as
select *
from users

create or replace function insted_of_del_user()
returns trigger as 
$$
begin
	update users
	set nickname = 'DELETE'
	where id = old.id;
	return old;
end
$$ language plpgsql

create trigger del_user
instead of delete on users_view
for each row 
execute procedure insted_of_del_user()

delete from users_view 
where id = 11

select *
from  users_view 
where id = 11

-- Защита
-- Процентное содержание аниме по жанрам
drop function  gen_anime();

create or replace function gen_anime()
returns table (genre text, proc bigint) as 
$$
declare
begin
	return query select a.genre, count(*)
	from anime a
	group by a.genre;
end
$$ language plpgsql;

select *
from gen_anime()
