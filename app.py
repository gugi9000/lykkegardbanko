from flask import Flask, render_template, request, redirect
from random import choice
import sqlite3


app = Flask(__name__)
app.secret_key = b"dette er en hemmelig streng"
app.url_map.strict_slashes = False
WTF_CSRF_SECRET_KEY = "a random string"


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
    if request.method == 'POST':
        return "Oops. We're not ready for that yet :-("

    numbers = list(range(1, 91))
    page = 'register'
    row1 = sorted([(i, numbers.pop(choice(range(len(numbers))))) for i in range(5)])
    row2 = sorted([(i, numbers.pop(choice(range(len(numbers))))) for i in range(5)])
    row3 = sorted([(i, numbers.pop(choice(range(len(numbers))))) for i in range(5)])
    rows = {1: row1, 2: row2, 3: row3}
    return render_template('register.html', page=page, title="Deltag!", rows=rows)


@app.route('/tilmeldte')
def show_players():
    page = 'players'
    numbers = list(range(1, 91))
    rows = list()
    for x in range(15):
        rows.append(numbers.pop(choice(range(len(numbers)))))
    players = [['Bjarke', 'Sørensen', sorted(rows)]]
    return render_template('players.html', page=page, title='Tilmeldte', players=players)


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
