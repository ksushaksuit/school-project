import os, sys
from io import StringIO
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

# Ответ на вопрос урока (код)
@app.route('/code/<id>/<step>', methods=['POST'])
def open_code(id, step):
    id = int(id)
    step = int(step)
    auth = session['student']
    answer = request.form['answer']
    counter = 0
    kolvo = 0
    if auth == None:
        return redirect('/')
    for l in lessons:
        if l['number'] == id:
            for s in l['lessons']:
                if s['num'] == step:
                    i_data = []
                    o_data = []
                    for j in s['io_data']:
                        i_data.append(j['input'])
                    for j in s['io_data']:
                        o_data.append(j['output'])
                    print(i_data, o_data)
                    counter = 0
                    kolvo = len(i_data)
                    for i in range(0, len(i_data)):
                        input_data = i_data[i]
                        output_data = o_data[i]
                        sys.stdin = StringIO(input_data)
                        old_stdout = sys.stdout
                        redirected_output = sys.stdout = StringIO()
                        try:
                            exec(answer)
                        except Exception as e:
                            print(e)
                        sys.stdout = old_stdout
                        result = redirected_output.getvalue()
                        print(str(result.strip()), str(output_data.strip()))
                        if str(result.strip()) == str(output_data.strip()):
                            counter += 1
                        print(counter)
                        if counter == 0:
                            description = 'Не выполнено'
                        elif counter != 0:
                            description = 'Успешно пройдено!'
                    return render_template('lesson.html', user=auth, l=l, step=step, counter=counter, kolvo=kolvo, d=description)
    return redirect('/student_education')


if __name__ == '__main__':
    app.run(debug=True)
