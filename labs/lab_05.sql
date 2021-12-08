-- Извлечение данных с помощью функций создания JSON
select row_to_json(anime) from labs.anime

-- Загрузка и сохранение JSON-документа
-- (В начале нужно поставить \copy)
copy (select row_to_json(anime) from anime)
to '/home/katy/bmstu/DB/bmstu-5sem-db/data_json/anime.json';

create table labs.anime_import(doc json);
--\copy labs.anime_import from '/home/katy/bmstu/DB/bmstu-5sem-db/data_json/anime.json'

select a.*
from anime_import, json_populate_record(null::labs.anime, doc) as a;

drop table anime_import


-- 3 - Создать таблицу, в которой будет атрибут(-ы) с типом XML или JSON, или
--добавить атрибут с типом XML или JSON к уже существующей таблице.
--Заполнить атрибут правдоподобными данными с помощью команд INSERT или UPDATE.

drop table banned_users;
create table banned_users (data json);

insert into banned_users
select * 
from json_object('{id_user, reason}', '{1, "Красноречиво выражался"}');

--4. Выполнить следующие действия:

--1. Извлечь XML/JSON фрагмент из XML/JSON документа
create table if not exists anime_id_title( id int, title text);
select * from anime_import, json_populate_record(null::anime_id_title, doc);

select id, title
from anime_import , json_populate_record(null::anime_id_title, doc)
order by title;

-- Оператор -> возвращает поле объекта JSON как JSON.
-- -> - выдаёт поле объекта JSON по ключу.
select * from anime_import;

select doc->'id' as id, doc->'title' as title
from anime_import;

--2. Извлечь значения конкретных узлов или атрибутов XML/JSON документа
drop table genres ;
create table genres(doc jsonb);

insert into genres values('{"id":1, "genres": {"japanese": "komodo", "general":"sport"}}');
insert into genres values('{"id":2, "genres": {"japanese": "shonen", "general":"thriller"}}');

select * from genres;

-- Извлекаем общий жанр у аниме
select doc->'id' as id, doc->'genres'->'general' as genre
from genres ;

--3. Выполнить проверку существования узла или атрибута
-- Проверка сеществования у аниме жанров
create or replace function get_genres(a_id jsonb)
returns text as $$
	select case 
		when count.cnt > 0
			then 'true'
		else 'false'
		end as comment
	from (select count(doc->'id') cnt
		  from genres
		  where doc->'id' @> a_id
		 ) as count;
$$ language sql;

select *from genres ;
select get_genres('1');

--4. Изменить XML/JSON документ
insert into genres values ('{"id":3, "genres": {"japanese": "shoujo", "general":"thriller"}}');

select * from genres ;

select doc || '{"id":33}'::jsonb
from genres;

update genres 
set doc = doc || '{"id": 33}'::jsonb
where (doc->'id')::int = 3;

select * from genres

--5. Разделить XML/JSON документ на несколько строк по узлам
drop table banned_users;
create table banned_users (doc json);

insert into banned_users values ('[{"id_user":11, "reason":"Неприличные комментарии под рецептом оливье"},
                                   {"id_user":3, "reason":"Писал спойлеры в комментариях"},
                                   {"id_user":5, "reason":"Душнила"}]');
                                  
select * from banned_users;

-- jsonb_array_elements - Разворачивает массив JSON в набор значений JSON.
select jsonb_array_elements(doc::jsonb)
from banned_users;

