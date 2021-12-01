import csv

from mimesis.schema import Field, Schema
from random import choice

def genre_description():
    genres = [None, 'Кодомо', 'Сёнэн', 'Сёдзё', 'Сэйнэн', 'Дзёсэй']
    f = Field()
    return {
        'genre' : choice(genres)
    }

schema = Schema(schema=genre_description)

with open('./data/genres.csv', 'a', newline='') as file:
    field_names = ['genre']
    writer = csv.DictWriter(file, fieldnames=field_names)

    # writer.writeheader()

    writer.writerows(schema.create(iterations=200))