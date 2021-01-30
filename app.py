from flask import Flask, render_template, request, redirect, url_for
from random import choice
import database


app = Flask(__name__)
app.secret_key = b"dette er en hemmelig streng"
app.url_map.strict_slashes = False
WTF_CSRF_SECRET_KEY = "a random string"


@app.template_filter()
def week_filter(gameweek):
    week = gameweek.replace('uge', '')
    return int(week)


app.jinja_env.filters['gameweek'] = week_filter


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
        values = list(fields.values())
        if not all([x for x in fields.values()]):
            errors.append('Alle felter skal udfyldes!')
        elif not all([x.isnumeric() for x in values[2:-1]]):
            errors.append('Alle tal skal være heltal..')

        # for k, v in fields.items():
        #     print(f"{k}: {v}")
        tal = set(values[2:17])
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
        if len(errors) == 0:
            previous = database.get_players(inputName=name, inputSurname=surname, gameweek=gameweek)
            if len(previous) == 0:
                database.add_registration(values)
                return redirect(url_for('show_players'))
            errors.append('En plade for valgte uge og navne findes allerede!!')
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
    players = database.get_players()
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
