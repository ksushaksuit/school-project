import os
from flask import Flask, render_template, request


app = Flask(__name__)

users = [
    {
        "name": "Иван Иванов",
        "email": "ivan@ivanov.ru",
        "password": '123',
        "role": 'Ученик',
        'rating': 5,
        'stars': 10,
        'teacher': 'Моргуненко Е.Ю'
    },
    {
        "name": "Олег",
        "email": "oleg@mail.ru",
        "password": '321',
        "role": 'Ученик',
        'rating': 4,
        'stars': 3,
        'teacher': 'Моргуненко Е.Ю'
    },
]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form_login', methods=['POST'])
def check_login_form():
    email = request.form.get('email')
    password = request.form.get('password')
    for u in users:
        if u['email'] == email and u['password'] == password:
            return render_template('student_cabinet.html', user=u, rating=users)


if __name__ == '__main__':
    # print(index_path)
    app.run(debug=True)
