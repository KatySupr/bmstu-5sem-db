import csv

from mimesis.schema import Field, Schema
import random

def studio_description():
    f = Field()
    return {
        'name': f('company'),
        'headquarters': f('address') + ' ' + f('city') + ' ' + f('country', allow_random=True),
        'founded': f('date', start=1940, end=1980),
        'employees' : random.randint(50, 500),
        'key_people': f('full_name')
    }


schema = Schema(schema=studio_description)
# data = schema.create(iterations=100)

with open('./data/studios.csv', 'a', newline='') as file:
    field_names = ['name', 'headquarters', 'founded', 'employees', 'key_people']
    writer = csv.DictWriter(file, fieldnames=field_names)

    # writer.writeheader()

    writer.writerows(schema.create(iterations=10))