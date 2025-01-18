import json

users = []

try:
    with open('data/users.json', 'r') as file:
        users = json.loads(file.read())
except:
    pass


def save_data():
    with open('data/users.json', 'w') as file:
        file.write(json.dumps(users, ensure_ascii=False))