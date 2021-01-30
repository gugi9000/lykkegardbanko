from flask import Flask, render_template
from random import choice

app = Flask(__name__)



@app.route('/')
def front_page():
    page = 'index'
    return render_template('index.html', page=page, title="Forside")


@app.route('/regler')
def show_rules():
    page = 'rules'
    return render_template('rules.html', page=page, title="Regler")


@app.route('/registrering', methods=['GET', 'POST'])
def register():
    numbers = list(range(1,91))
    page = 'register'
    row1 = [(i, choice(numbers)) for i in range(5)]
    row2 = [(i, choice(numbers)) for i in range(5)]
    row3 = [(i, choice(numbers)) for i in range(5)]
    rows = {1: sorted(row1), 2: sorted(row2), 3: sorted(row3)}
    return render_template('register.html', page=page, title="Deltag!", rows=rows)


@app.route('/vinder')
def banko():
    page = 'banko'
    return render_template('banko.html', page=page, title="Banko!")


@app.route('/vindere')
def show_winners():
    page = 'winners'
    return render_template('winners.html', page=page, title="Vindere")


if __name__ == '__main__':
    app.run()
