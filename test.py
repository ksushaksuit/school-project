import os, sys
from io import StringIO
from flask import Flask, render_template, request, session, redirect
from uroki import lessons

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
    print(auth)
    return render_template('student_cabinet.html', user=auth, users=users)

# Страница учителя
@app.route('/teacher')
def teacher():
    auth = session['teacher']
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
    code = ''
    if auth == None:
        return redirect('/')
    for l in lessons:
        if l['number'] == id:
            text_q = []
            quest_q = []
            code_q = []
            for j in l['lessons']:
                if j['type'] == 'text':
                    text_q.append(j)
                if j['type'] == 'question':
                    quest_q.append(j)
                if j['type'] == 'code':
                    code_q.append(j)
            return render_template('lesson.html', user=auth, l=l, step=step, text=text_q, quest=quest_q, code_q=code_q)
    return redirect('/student_education')

# Ответ на вопрос урока
@app.route('/answer/<id>/<step>', methods=['POST'])
def open_answer(id, step):
    id = int(id)
    step = int(step)
    auth = session['student']
    answer = request.form['answer']
    if answer == 'True':
        session['student']['stars'] += 1
        print(session['student'])
    if auth == None:
        return redirect('/')
    for l in lessons:
        if l['number'] == id:
            text_q = []
            quest_q = []
            code_q = []
            for j in l['lessons']:
                if j['type'] == 'text':
                    text_q.append(j)
                if j['type'] == 'question':
                    quest_q.append(j)
                if j['type'] == 'code':
                    code_q.append(j)
            return render_template('lesson.html', user=auth, l=l, step=step, is_true=answer, text=text_q, quest=quest_q, code_q=code_q)
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
    user_output = []
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
                        user_output.append(result)
                        print(str(result.strip()), str(output_data.strip()))
                        if str(result.strip()) == str(output_data.strip()):
                            counter += 1
                        print(counter)
                        if counter == 0:
                            description = 'Не выполнено.'
                        elif counter != len(i_data) and counter != 0:
                            description = 'Частично пройдено. Результат не засчитан.'
                        elif counter == len(i_data):
                            description = 'Пройдено.'
                            session['student']['stars'] += 1
                    text_q = []
                    quest_q = []
                    code_q = []
                    for j in l['lessons']:
                        if j['type'] == 'text':
                            text_q.append(j)
                        if j['type'] == 'question':
                            quest_q.append(j)
                        if j['type'] == 'code':
                            code_q.append(j)
                    print(i_data)
                    return render_template('lesson.html', user=auth, l=l, step=step, counter=counter, kolvo=kolvo, text=text_q, quest=quest_q, code_q=code_q, d=description, code=answer, user_output=user_output)
    return redirect('/student_education')


if __name__ == '__main__':
    app.run(debug=True)
