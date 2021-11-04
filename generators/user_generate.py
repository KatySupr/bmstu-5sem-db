import csv

from mimesis.schema import Field, Schema

def user_description():
    f = Field()
    return {
        'nickname': f('username'),
        'created_at': f('timestamp', posix=False),
        'country': f('country', allow_random=True),
        'email' : f('email'),
        'sex': f('gender')
    }


schema = Schema(schema=user_description)
# data = schema.create(iterations=100)

with open('./data/users.csv', 'a', newline='') as file:
    field_names = ['nickname', 'created_at', 'country', 'email', 'sex']
    writer = csv.DictWriter(file, fieldnames=field_names)

    # writer.writeheader()
    
    writer.writerows(schema.create(iterations=100))