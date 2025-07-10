from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import openpyxl
from openpyxl import Workbook, load_workbook

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

ORDERS_DIR = 'orders'
EXCEL_FILE = os.path.join(ORDERS_DIR, 'orders.xlsx')

def save_orders_to_excel(cart):
    if not cart:
        return
    if not os.path.exists(ORDERS_DIR):
        os.makedirs(ORDERS_DIR)
    try:
        wb = load_workbook(EXCEL_FILE)
        ws = wb.active
    except FileNotFoundError:
        wb = Workbook()
        ws = wb.active
        ws.append(['Мед', 'Кількість (кг)', "Ім'я", 'Телефон', 'Адреса нової пошти'])
    for item in cart:
        ws.append([
            item.get('honey', ''),
            item.get('amount', ''),
            item.get('name', ''),
            item.get('phone', ''),
            item.get('address', '')
        ])
    wb.save(EXCEL_FILE)

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
        address = request.form.get('address')
        amount = request.form.get('amount')
        if not name or not phone or not amount or not address:
            flash('Будь ласка, заповніть всі поля!', 'danger')
        else:
            cart = session.get('cart', [])
            cart.append({'honey': honey['name'], 'amount': amount, 'name': name, 'phone': phone, 'address': address})
            session['cart'] = cart
            flash('Товар додано до корзини!', 'success')
            return redirect(url_for('cart'))
    return render_template('honey.html', honey=honey)

@app.route('/cart', methods=['GET'])
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/place_order', methods=['POST'])
def place_order():
    cart = session.get('cart', [])
    if not cart:
        flash('Корзина порожня!', 'danger')
        return redirect(url_for('cart'))
    save_orders_to_excel(cart)
    session['cart'] = []
    flash('Замовлення оформлено та збережено у Excel!', 'success')
    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    flash('Корзину очищено!', 'success')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True) 