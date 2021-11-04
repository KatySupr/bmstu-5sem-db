import csv

from mimesis.schema import Field, Schema
from random import randint

def user_description():
    f = Field()
    return {
        'id_anime': randint(1, 1100),
        'id_user': randint(1, 1000),
        'start': f('timestamp', posix=False, start=2018, end=2019),
        'end' : f('timestamp', posix=False, start=2020, end=2021),
        'if_finish': randint(0, 1)
    }


schema = Schema(schema=user_description)
# data = schema.create(iterations=100)

with open('./data/viewed.csv', 'a', newline='') as file:
    field_names = ['id_anime', 'id_user', 'start', 'end', 'if_finish']
    writer = csv.DictWriter(file, fieldnames=field_names)

    # writer.writeheader()
    
    writer.writerows(schema.create(iterations=100))