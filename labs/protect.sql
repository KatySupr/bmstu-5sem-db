ALTER TABLE labs.anime ADD COLUMN genre text default 'сенэн-ай' not null;

ALTER TABLE labs.users ADD COLUMN favorite_genre text;

-- аниме с максимальным рейтингом за 21 год

select title, start_at, end_at, rating
from labs.anime a
where start_at >= '2010-01-01' and rating >= (
	select avg(rating)
	from labs.anime
)
order by rating desc