# Создать базовый шаблон для интернет-магазина,
# содержащий общие элементы дизайна (шапка, меню, подвал),
# и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
# Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clothing/')
def clothing():
    return render_template('clothing.html')


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/child/')
def child():
    return render_template('child.html')

# было
# @app.route('/jackets/')
# def jackets():
#     return render_template('jackets.html')


# Доделано. Теперь передача данных в контекст
@app.route('/jackets')
def jackets():
    jackets_list = [
        {
            'photo': '/static/jacket1.jpeg',
            'price': '1000 рублей',
            'description': 'Отличная куртка для холодной погоды.'
        },
        {
            'photo': '/static/jacket2.jpeg',
            'price': '1500 рублей',
            'description': 'Стильная куртка для повседневной носки.'
        },
        {
            'photo': '/static/jacket3.jpeg',
            'price': '1200 рублей',
            'description': 'Удобная и практичная куртка.'
        }
    ]
    return render_template('jackets.html', jackets=jackets_list)


if __name__ == '__main__':
    app.run()


if __name__ == '__main__':
    app.run(debug=True)