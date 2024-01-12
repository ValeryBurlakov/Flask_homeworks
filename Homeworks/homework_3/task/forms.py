from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя:',
                           validators=[DataRequired(),
                                       Regexp("^[a-zA-Zа-яА-Я]+$",
                                              message="Имя должно содержать только буквы")])
    password = PasswordField('Пароль:', validators=[
        DataRequired(), Length(min=8)])
    terms = BooleanField("Я согласен с условиями и политикой конфиденциальности.",
                         validators=[DataRequired()])


def validate_birthday(form, field):
    today = datetime.now().date()
    if field.data.date() > today:
        raise ValidationError('Дата рождения не может быть в будущем')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired(),
                                                            Regexp("^[a-zA-Zа-яА-Я]+$",
                                                                   message="Имя должно содержать только буквы")])
    usersurname = StringField('Фамилия пользователя:',
                              validators=[DataRequired(),
                                          Regexp("^[a-zA-Zа-яА-Я]+$", message="Фамилия должна содержать только буквы")])
    email = StringField('Email:', validators=[DataRequired(), Email(message="некорректный email")])
    password = PasswordField('Пароль:',
                             validators=[DataRequired(),
                                         Length(min=8),
                                         Regexp('(?=.*[a-z])(?=.*[0-9])',
                                                message="Ошибка! Нужны цифры и буквы!")])
    confirm_password = PasswordField('Повторите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message="пароли не совпадают")])
    birthday = DateTimeField('Дата рождения (dd.mm.yyyy)', format='%d.%m.%Y',
                             validators=[DataRequired(message="некорректная дата"), validate_birthday])
    terms = BooleanField("Я согласен с условиями и политикой конфиденциальности.",
                         validators=[DataRequired()])
