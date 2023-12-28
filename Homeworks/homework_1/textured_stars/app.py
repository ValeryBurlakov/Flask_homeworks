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


@app.route('/shoes/')  # переход на contact
def shoes():
    return render_template('shoes.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/child/')
def child():
    return render_template('child.html')


@app.route('/jackets/')
def jackets():
    return render_template('jackets.html')


if __name__ == '__main__':
    app.run(debug=True)