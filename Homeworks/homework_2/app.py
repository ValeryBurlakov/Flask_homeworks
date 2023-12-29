# Task_5. Создать страницу, на которой будет форма для ввода двух
# чисел и выбор операции (сложение, вычитание, умножение
# или деление) и кнопка "Вычислить"
# 📌 При нажатии на кнопку будет произведено вычисление
# результата выбранной операции и переход на страницу с
# результатом.

# Task_9. Создать страницу, на которой будет форма для ввода имени
# и электронной почты
# 📌 При отправке которой будет создан cookie файл с данными
# пользователя
# 📌 Также будет произведено перенаправление на страницу
# приветствия, где будет отображаться имя пользователя.
# 📌 На странице приветствия должна быть кнопка "Выйти"
# 📌 При нажатии на кнопку будет удален cookie файл с данными
# пользователя и произведено перенаправление на страницу
# ввода имени и электронной почты.
from pathlib import Path, PurePath
from re import split

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.context_processor
def menu():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Task 1', 'url': url_for("task_1")},
        {'name': 'Task 2', 'url': url_for("task_2")},
        {'name': 'Task 3', 'url': url_for("task_3")},
        {'name': 'Task 4', 'url': url_for("task_4")},
        {'name': 'Homework_2, Task 5', 'url': url_for("task_5")},
        {'name': 'Task 6', 'url': url_for("task_6")},
        {'name': 'Task 7', 'url': url_for("task_7")},
        {'name': 'Task 8', 'url': url_for("task_8")},
        {'name': 'Homework_2, Task 9', 'url': url_for("task_9")}
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task_1', methods=['GET', 'POST'])
def task_1():
    if request.method == 'POST':
        return redirect(url_for('hello', name='User'))
    return render_template('task_1.html')


@app.route('/task_2')
def task_2():
    return render_template('task_2.html')


# ===============================Homework_2
@app.route('/hello')
def hello():
    user_data = request.cookies.get('user_data')
    if user_data:
        name, email = user_data.split(':')
        return render_template('hello.html', name=name, email=email)
    else:
        flash('Ошибка, нужно вводить имя и электронную почту', 'danger')
        return redirect(url_for('task_9'))


# ===============================Homework_2
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('task_9')))
    response.set_cookie('user_data', '', expires=0)  # Delete the cookie
    return response


@app.route('/task_2_upload', methods=['GET', 'POST'])
def task_2_upload():
    if request.method == 'POST':
        image = request.files.get('image')
        file_name = secure_filename(image.filename)
        Path(Path.cwd(), 'static', 'uploads').mkdir(exist_ok=True)
        # сохранение изображения
        image.save(PurePath.joinpath(Path.cwd(), 'static', 'uploads', file_name))
        return (f"""Файл {file_name} загружен на сервер<br>
        <a href='{url_for('task_2_upload')}'>назад</a>""")

    return render_template('form_task_2.html')


@app.route('/task_3', methods=['GET', 'POST'])
def task_3():
    login = 'l'
    password = 'p'
    if request.method == 'POST':
        login_new = request.form.get('login')
        password_new = request.form.get('password')
        if login_new == login and password_new == password:
            return redirect(url_for('hello', name=login))
        else:
            flash('Ошибка', 'danger')
            return redirect(url_for('task_3'))
    return render_template('task_3.html')


@app.route('/task_4', methods=['GET', 'POST'])
def task_4():
    if request.method == 'POST':
        text = request.form.get('text').strip()
        words = split(r'[,.\s]+', text)
        return f'Слов: {len(words)}'
    return render_template('task_4.html')


# ===============================Homework_2
@app.route('/task_5', methods=['GET', 'POST'])
def task_5():
    if request.method == 'POST':
        res = 0
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        operation = request.form.get('operation')
        if operation == 'addition':
            res = num1 + num2
        elif operation == 'substraction':
            res = num1 - num2
        elif operation == 'multiplication':
            res = num1 * num2
        elif operation == 'division':
            res = int(num1 / num2)
        return f'Результат операции "{operation}" чисел {num1} и {num2} = {str(res)}'
    return render_template('task_5.html')


@app.route('/task_6', methods=['GET', 'POST'])
def task_6():
    if request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        if age > 18:
            return render_template('index.html')
        else:
            return render_template('404.html')
    return render_template('task_6.html')


@app.route('/task_7', methods=['GET', 'POST'])
def task_7():
    if request.method == 'POST':
        num = int(request.form.get('num'))
        return f'Результат {num**2}'
    return render_template('task_7.html')


@app.route('/task_8', methods=['GET', 'POST'])
def task_8():
    if request.method == 'POST':
        if not request.form.get('name'):
            flash('Вы не ввели имя', 'danger')
            return redirect(url_for('task_8'))
        name = request.form.get('name')
        flash('Всё в порядке', 'success')
        return f'Привет {name}!'
    return render_template('task_8.html')


# ===============================Homework_2
# @app.route('/task_9', methods=['GET', 'POST'])
# def task_9():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         response = make_response(redirect(url_for('hello')))
#         response.set_cookie('user_data', f'{name}:{email}')
#         return response
#     return render_template('task_9.html')
@app.route('/task_9', methods=['GET', 'POST'])
def task_9():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:  # Проверяем наличие имени и электронной почты
            response = make_response(redirect(url_for('hello')))
            response.set_cookie('user_data', f'{name}:{email}')
            flash('Всё в порядке', 'success')
            return response
        else:
            flash('укажите имя и почту !', 'danger')  # Добавляем сообщение об ошибке
            return render_template('task_9.html')
    return render_template('task_9.html')


if __name__ == '__main__':
    app.run(debug=True)
