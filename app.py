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
    errors = list()
    page = 'register'
    name, surname, gameweek = None, None, None
    if request.method == 'POST':
        fields = dict(request.form.items())
        if not all([x for x in fields.values()]):
            errors.append('Alle felter skal udfyldes!')

        values = list(fields.values())
        for k, v in fields.items():
            print(f"{k}: {v}")
        tal = set(values[2:17])
        print(tal)
        if len(tal) != 15:
            errors.append('Der skal være 15 forskellige tal!')

        row1 = [(i, num) for i, num in enumerate(values[2:7])]
        row2 = [(i, num) for i, num in enumerate(values[7:12])]
        row3 = [(i, num) for i, num in enumerate(values[12:17])]
        if not fields.get('gameweek', None):
            errors.append('Vælg en uge at spille for!')
        name = fields.get('inputName', None)
        surname = fields.get('inputSurname', None)
        gameweek = fields.get('gameweek', None)
    else:
        numbers = list(range(1, 91))
        row1 = [(i, numbers.pop(choice(range(len(numbers))))) for i in range(5)]
        row2 = [(i, numbers.pop(choice(range(len(numbers))))) for i in range(5)]
        row3 = [(i, numbers.pop(choice(range(len(numbers))))) for i in range(5)]
    rows = {1: row1, 2: row2, 3: row3}
    return render_template('register.html', page=page, title="Deltag!", rows=rows, name=name, gameweek=gameweek, surname=surname, errors=errors)


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
