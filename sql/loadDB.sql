copy labs.users (nickname, created_at, country, email, sex) from '/home/katy/bmstu/DB/data/users.csv'
	with delimiter ',' csv header;
	
copy labs.studio (name, headquarters, founded, employees, key_people) from '/home/katy/bmstu/DB/data/studios.csv'
	with delimiter ',' csv header;
	
copy labs.anime (title, studio_id, episodes, mpaa, start_at, end_at, rating) from '/home/katy/bmstu/DB/data/animes.csv'
	with delimiter ',' csv header;
	
copy labs.viewed_anime (id_anime, id_user, start_at, end_at, if_finish) from '/home/katy/bmstu/DB/data/viewed.csv'
	with delimiter ',' csv header;