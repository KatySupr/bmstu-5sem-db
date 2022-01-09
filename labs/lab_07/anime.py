class anime():
    id = int()
    title = str()
    studio_id = int()
    episodes = int()
    mpaa = str()
    start_at = str()
    end_at = str()
    rating = float()
    genre = str()

    def __init__(self, id, title, studio_id, episodes, mpaa, start_at, end_at, rating, genre):
        self.id = id
        self.title = title
        self.studio_id = studio_id
        self.episodes = episodes
        self.mpaa = mpaa
        self.start_at = start_at
        self.end_at = end_at
        self.rating = rating
        self.genre = genre

    def get(self):
        return {'id': self.id,
                'title': self.title,
                'studio_id': self.studio_id,
                'episodes': self.episodes,
                'mpaa': self.mpaa,
                'start_at': self.start_at,
                'end_at': self.end_at,
                'rating': self.rating,
                'genre': self.genre}

    def __str__(self) -> str:
        return f"{self.id:<3} {self.title:<70} {self.studio_id:<4} {self.episodes:<5} {self.mpaa:<5} {self.start_at:<12} {self.end_at:<12} {self.rating:<4} {self.genre:<10}"

def create_animes(file_name):
    # Содает коллекцию объектов.
    # Загружая туда данные из файла file_name.
    file = open(file_name, 'r')
    animes = []

    for line in file:
        arr = line.split(',')
        arr[0], arr[2], arr[3] = int(arr[0]), int(arr[2]), int(arr[3])
        arr[7] = float(arr[7])
        animes.append(anime(*arr).get())

    return animes
        

class user():
    # Структура полностью соответствует таблице users.
    id = int()
    nickname = str()
    age = int()
    sex = str()
    number_of_hours = int()
    id_device = int()

    def __init__(self, id, nickname, age, sex, number_of_hours, id_device):
        self.id = id
        self.nickname = nickname
        self.age = age
        self.sex = sex
        self.number_of_hours = number_of_hours
        self.id_device = id_device

    def get(self):
        return {'id': self.id, 'nickname': self.nickname, 'age': self.age,
                'sex': self.sex, 'number_of_hours': self.number_of_hours, 'id_device': self.id_device}

    def __str__(self):
        return f"{self.id:<2} {self.nickname:<20} {self.age:<5} {self.sex:<5} {self.number_of_hours:<15} {self.id_device:<15}"



def create_users(file_name):
    # Содает коллекцию объектов.
    # Загружая туда данные из файла file_name.
    file = open(file_name, 'r')
    users = list()

    for line in file:
        arr = line.split(',')
        arr[0], arr[2], arr[4], arr[5] = int(
            arr[0]), int(arr[2]), int(arr[4]), int(arr[5])
        users.append(user(*arr).get())

    return users