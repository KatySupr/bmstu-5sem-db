create table if not exists animes_json (doc JSON);

insert into animes_json
select * from anime_import

select * from animes_json;