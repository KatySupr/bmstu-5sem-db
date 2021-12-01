import csv

from mimesis.schema import Field, Schema
from random import randint

def genre_description():
    f = Field()
    return {
        'id_friend' : randint(1, 1000)
    }

schema = Schema(schema=genre_description)

with open('./data/friends.csv', 'a', newline='') as file:
    field_names = ['id_friend']
    writer = csv.DictWriter(file, fieldnames=field_names)

    # writer.writeheader()

    writer.writerows(schema.create(iterations=1))