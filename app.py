from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

HONEY_TYPES = [
    {
        'slug': 'acacia',
        'name': "Акацієвий мед",
        'desc': "Світлий, ніжний, з легким ароматом акації. Дуже корисний для дітей.",
        'img': 'acacia.jpg'
    },
    {
        'slug': 'buckwheat',
        'name': "Гречаний мед",
        'desc': "Темний, насичений смак, багатий на залізо. Рекомендується при анемії.",
        'img': 'buckwheat.jpg'
    },
    {
        'slug': 'sunflower',
        'name': "Соняшниковий мед",
        'desc': "Яскравий, золотистий, з приємною кислинкою. Дуже популярний в Україні.",
        'img': 'sunflower.jpg'
    },
    {
        'slug': 'herbs',
        'name': "Мед різнотрав'я",
        'desc': "Ароматний, зібраний з різних польових квітів. Має широкий спектр корисних властивостей.",
        'img': 'herbs.jpg'
    },
]

@app.route('/')
def home():
    return render_template('index.html', honeys=HONEY_TYPES)

@app.route('/honey/<slug>', methods=['GET', 'POST'])
def honey_page(slug):
    honey = next((h for h in HONEY_TYPES if h['slug'] == slug), None)
    if not honey:
        return "Мед не знайдено", 404
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        amount = request.form.get('amount')
        if not name or not phone or not amount:
            flash('Будь ласка, заповніть всі поля!', 'danger')
        else:
            flash('Дякуємо за замовлення! Ми звʼяжемося з вами найближчим часом.', 'success')
            return redirect(url_for('honey_page', slug=slug))
    return render_template('honey.html', honey=honey)

if __name__ == '__main__':
    app.run(debug=True) 