from flask import Flask, render_template

app = Flask(__name__)

HONEY_TYPES = [
    {
        'name': "Акацієвий мед",
        'desc': "Світлий, ніжний, з легким ароматом акації. Дуже корисний для дітей.",
        'img': 'acacia.jpg'
    },
    {
        'name': "Гречаний мед",
        'desc': "Темний, насичений смак, багатий на залізо. Рекомендується при анемії.",
        'img': 'buckwheat.jpg'
    },
    {
        'name': "Соняшниковий мед",
        'desc': "Яскравий, золотистий, з приємною кислинкою. Дуже популярний в Україні.",
        'img': 'sunflower.jpg'
    },
    {
        'name': "Мед різнотрав'я",
        'desc': "Ароматний, зібраний з різних польових квітів. Має широкий спектр корисних властивостей.",
        'img': 'herbs.jpg'
    },
]

@app.route('/')
def home():
    return render_template('index.html', honeys=HONEY_TYPES)

if __name__ == '__main__':
    app.run(debug=True) 