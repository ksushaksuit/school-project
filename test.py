import os
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = 'blablabla'

# Имитация (временная БД пользователей)
users = [
    {
        "name": "Иван Иванов",
        "email": "ivan@ivanov.ru",
        "password": '123',
        "role": 'Ученик',
        'rating': 5,
        'stars': 10,
        'solved': [],
        'teacher': 'Моргуненко Е.Ю'
    },
    {
        "name": "Олег",
        "email": "oleg@mail.ru",
        "password": '321',
        "role": 'Ученик',
        'rating': 4,
        'stars': 3,
        'solved': [],
        'teacher': 'Моргуненко Е.Ю'
    },
    {
        "name": "Моргуненко Е.Ю",
        "email": "m@eu.ru",
        "password": '12345',
        "role": 'Учитель',
        'solved': [],
        'rating': 4,
        'stars': 3,
    }
]

# Имитация (временная БД пользователей)
lessons = [
    {
        "number": 1,
        "title": 'print(), input(), int(input()) - что и как',
        'lessons': [
            {
                'num': 1,
                'type': 'text',
                'text': 'print() - это вывод. <b>Запомните!</b> '
            },
            {
                'num': 2,
                'type': 'text',
                'text': 'input() - это ввод'
            },
            {
                'num': 3,
                'type': 'question',
                'text': 'Какая функция отвечает за вывод?',
                'answer': [
                    {
                        "text": 'print',
                        'is_true': True
                    },
                    {
                        "text": 'input',
                        'is_true': False
                    },
                    {
                        "text": 'vvod',
                        'is_true': False
                    }
                ]
            },
            {
                'num': 4,
                'type': 'code',
                'text': 'Выведите на экран "Hello, world!"',
                'answer': 'Hello, world!',
            },
        ]
    },
    {
        "number": 2,
        "title": 'Переменные - что и как',
        'lessons': [
            {
                'num': 1,
                'type': 'text',
                'text': 'print() - это вывод.'
            },
            {
                'num': 2,
                'type': 'text',
                'text': 'input() - это ввод'
            },
            {
                'num': 3,
                'type': 'question',
                'text': 'Какая функция отвечает за вывод?',
                'answer': 'print'
            },
            {
                'num': 4,
                'type': 'code',
                'text': 'Выведите на экран "Hello, world!"',
                'answer': 'Hello, world!',
            },
        ]
    },

]


@app.route('/')
def home():
    return render_template('index.html')

# Логин учителя и ученика
@app.route('/form_login', methods=['POST'])
def check_login_form():
    email = request.form.get('email')
    password = request.form.get('password')
    for u in users:
        if u['email'] == email and u['password'] == password:
            if u['role'] == 'Ученик':
                session['student'] = u
                return redirect('/student')
            if u['role'] == 'Учитель':
                session['teacher'] = u
                return redirect('/teacher')

# Страница ученика
@app.route('/student')
def student():
    auth = session['student']
    return render_template('student_cabinet.html', user=auth, users=users)

# Страница учителя
@app.route('/teacher')
def teacher():
    auth = session['student']
    return render_template('teacher_cabinet.html', user=auth, users=users)

# Список уроков для ученика
@app.route('/student_education')
def student_education():
    auth = session['student']
    if auth == None:
        return redirect('/')
    return render_template('student_education.html', user=auth, lessons=lessons)

# Урок (открывается по Id урока и шагу)
@app.route('/lessons/<id>/<step>')
def open_lesson(id, step):
    id = int(id)
    step = int(step)
    auth = session['student']
    if auth == None:
        return redirect('/')
    for l in lessons:
        if l['number'] == id:
            return render_template('lesson.html', user=auth, l=l, step=step)
    return redirect('/student_education')

# Ответ на вопрос урока
@app.route('/answer/<id>/<step>', methods=['POST'])
def open_answer(id, step):
    id = int(id)
    step = int(step)
    auth = session['student']
    answer = request.form['answer']
    if auth == None:
        return redirect('/')
    for l in lessons:
        if l['number'] == id:
            return render_template('lesson.html', user=auth, l=l, step=step, is_true=answer)
    return redirect('/student_education')


if __name__ == '__main__':
    app.run(debug=True)
