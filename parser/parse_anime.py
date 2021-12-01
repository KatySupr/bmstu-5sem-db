import requests
from bs4 import BeautifulSoup
from parse import parse
from mimesis import Generic
import random
import csv

def mpaa(mpaa):
    mpaa_array = ('G', 'PG', 'PG-13', 'R', 'NC-17')
    if mpaa not in mpaa_array:
        mpaa = random.choice(mpaa_array)

    return mpaa

def mounth_parse(mounth):
    if mounth[:-1] == 'январ':
        return 1
    if mounth[:-1] == 'феврал':
        return 2
    if mounth[:-1] == 'март':
        return 3
    if mounth[:-1] == 'апрел':
        return 4
    if mounth[:-1] == 'ма':
        return 5
    if mounth[:-1] == 'июн':
        return 6
    if mounth[:-1] == 'июл':
        return 7
    if mounth[:-1] == 'август':
        return 8
    if mounth[:-1] == 'сентбр':
        return 9
    if mounth[:-1] == 'октябр':
        return 10
    if mounth[:-1] == 'ноябр':
        return 11
    if mounth[:-1] == 'декабр':
        return 12
    return 1

def date_parse(dat: str):
    try:
        start, end = parse('с {} по {}', dat)
        start = start.split()
        end = end.split()

        start = Generic().datetime.date(int(start[2]), mounth_parse(start[1]), int(start[0]))
        end = Generic().datetime.date(int(end[2]), mounth_parse(end[1]), int(end[0]))
    except BaseException:
        start = Generic().datetime.date(start=1985, end=1995)
        end = Generic().datetime.date(start=1996, end=2021)
    
    return start, end

genres = ['Кодомо', 'Сёнэн', 'Сёдзё', 'Сэйнэн', 'Дзёсэй']

with open('./links/anime_links/13.txt', 'r') as f:
    with open('./data/animes_new.csv', 'a', newline='') as file:
        field_names = ['title', 'studio_id', 'episodes', 'mpaa', 'start', 'end', 'rating', 'genre']
        writer = csv.DictWriter(file, fieldnames=field_names)

        # writer.writeheader()

        for line in f.readlines():
            anime = dict()

            url = line[:-1]
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
                
            title = soup.find('div', class_='anime-title')
            if title:
                title = title.find('h1').text
                anime['title'] = title
            else:
                continue

            try:
                anime['rating'] = float(soup.find('span', class_='rating-value').text.replace(',', '.'))
            except BaseException:
                anime['rating'] = round(random.uniform(1, 10), 1)

            anime['studio_id'] = random.randint(1, 1000)

            anime_info = soup.find_all('dd', class_='col-6 col-sm-8 mb-1')
            if anime_info:
                episodes = anime_info[1].text
                try:
                    anime['episodes'] = int(episodes)
                except BaseException:
                    anime['episodes'] = random.randint(10, 20)

                data = anime_info[5].text
                if data:
                    anime['start'], anime['end'] = date_parse(data)
                else:
                    anime['start'] = Generic().datetime.date(start=1999, end=2015)
                    anime['end'] = Generic().datetime.date(start=2015, end=2021)

                anime['mpaa'] = mpaa(anime_info[6].text)

                anime['genre'] = random.choice(genres)

            writer.writerow(anime)
            print(anime)
