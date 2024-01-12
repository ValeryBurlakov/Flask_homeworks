# Создайте форму регистрации пользователей в приложении Flask.
# Форма должна содержать поля "Имя", "Фамилия", "Email",
# "Пароль" и кнопку "Зарегистрироваться". +++
# При отправке формы данные должны валидироваться на следующие условия:
# ○ Все поля обязательны для заполнения. +++
# ○ Поле email должно быть валидным email адресом. +++
# ○ Поле пароль должно содержать не менее 8 символов, включая хотя бы одну букву и
# одну цифру. +++
# ○ Поле подтверждения пароля должно совпадать с полем пароля. +++
# ○ Если данные формы не прошли валидацию, на странице должна быть выведена
# соответствующая ошибка. +++
# ○ Если данные формы прошли валидацию, на странице должно быть выведено
# сообщение об успешной регистрации. +++
# ○ При отправке формы данные должны сохраняться в базе
# данных, а пароль должен быть зашифрован. +++

from flask import Flask, render_template, url_for, request, session, redirect
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from forms import RegistrationForm, LoginForm
from models import db, Student, Book, Mark
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seminar3.db'
db.init_app(app)
migrate = Migrate(app, db)

app.config[
    'SECRET_KEY'] = b'b0ee5a2c6515091072087d57c6693be951cd9fc4629e5e66324c8c33331b5768'
csrf = CSRFProtect(app)


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Вход', 'url': url_for("login")},
        {'name': 'Регистрация', 'url': url_for("registration")}
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {'alert_message': "Такого пользователя не существует, повторите вход или зарегистрируйтесь"}
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Student.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                context = {'username': username}
                # Вход прошел успешно
                return render_template('welcome.html', form=form, **context)
        return render_template('login.html', form=form, **context)
    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    context = {'alert_message': "Добро пожаловать!"}
    form = RegistrationForm()
    username = form.username.data
    usersurname = form.usersurname.data
    email = form.email.data
    password = form.password.data
    birthday = form.birthday.data
    terms = form.terms.data
    if request.method == 'POST' and form.validate():
        if Student.query.filter(Student.username == username).all() or \
                Student.query.filter(Student.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('registration.html', form=form, **context)
        else:
            # можно захешировать методом sha256, пишут менее ресурсозатратный
            # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            hashed_password = generate_password_hash(password)
            #print(Student.query.filter(Student.username == username).all())
            new_user = Student(username=username, usersurname=usersurname, email=email,
                               password=hashed_password, birthday=birthday,
                               terms=terms)
            db.session.add(new_user)
            db.session.commit()
            return render_template('registration.html', form=form, **context)
    return render_template('registration.html', form=form)

# set FLASK_APP=run.py
# flask db init
# flask db migrate
# flask db upgrade
if __name__ == '__main__':
    app.run(debug=True)