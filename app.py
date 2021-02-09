from flask import Flask, render_template, request, redirect, url_for
from random import choice, shuffle
import database


app = Flask(__name__)
app.secret_key = b"dette er en hemmelig streng"
app.url_map.strict_slashes = False
WTF_CSRF_SECRET_KEY = "a random string"

draw_1 = [59, 66, 31, 28, 60, 19, 30, 46, 70, 41,
          20, 33, 16, 76, 49, 54, 36, 23, 90, 1, ]
draw_2 = [3, 56, 22, 52, 50, 64, 45, 13, 87, 18, ]
draw_3 = [75, 34, 79, 84, 4, 43, 63, 42, 25, 72, ]  # Heidi på 79, en række - Jeanett på 43, en række
draw_4 = [74, 80, 24, 55, 32, 12, 5, 53, 2, 61, ]   # Jeanett på 2 to rækker
draw_5 = [6, 57, 62, 40, 39, 77, 83, 85, 89, 81, ]
draw_6 = [26, 86, 71, 44, 67, 73, 48, 58, 65, 7, ]
draw_7 = [69, 88, 51, 27, 21, 47, 38, 82, 37, 10]  # Laura banko på 82 - fuld plade
not_drawn = [68, 14, 11, 8, 29, 35, 78, 15, 17, 9]  # Mads og Jeanett hele pladen på 68
draw = draw_1 + draw_2 + draw_3 #+ draw_4 + draw_5 + draw_6 + draw_7
latest_draw = draw_3

sponsorer = [
    ['FairIT.png', 'Fair IT A/S'],
    ['danbolig.png', 'Danbolig Holbæk'],
    ['liljehoj.jpg','Liljehøj'],
    ['lykkegard.png','Lykkegard'],
    ['massorskolen.png','Massørskolen-Fyn'],
    ['parasport.png','Parasport Danmark'],
    ['revisorgaarden.png','RevisorGården Holbæk'],
    ['slagterknabstrup.png','Slageren i Knabstrup'],
    ['sparekassen.png','Sparekassen Sjælland-Fyn'],
    ['superbrugsenasnaes.png','Superbrugsen Asnæs'],
    ]



@app.template_filter()
def week_filter(gameweek):
    week = gameweek.replace('uge', '')
    return int(week)


@app.template_filter()
def drawn(number):
    if number in draw:
        return f' class="table-success"'
    return ''


app.jinja_env.filters['gameweek'] = week_filter
app.jinja_env.filters['drawn'] = drawn


@app.route('/')
def front_page():
    page = 'index'
    shuffle(sponsorer)
    return render_template('index.html', page=page, title="Forside", drawn=latest_draw, sponsorer=sponsorer)


@app.route('/regler')
def show_rules():
    page = 'rules'
    shuffle(sponsorer)
    return render_template('rules.html', page=page, title="Regler", sponsorer=sponsorer)


@app.route('/videoer')
def show_videos():
    page = 'videoer'
    shuffle(sponsorer)
    return render_template('videos.html', page=page, title="Tidligere videoer", sponsorer=sponsorer)


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
        if fields.get('gameweek', None) == 'uge6':
            errors.append('Der kan ikke længere registreres plader for uge 6.')
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
    shuffle(sponsorer)
    return render_template('register.html', page=page, title="Deltag!", rows=rows, name=name, gameweek=gameweek, surname=surname, errors=errors, sponsorer=sponsorer)


@app.route('/tilmeldte')
def show_players():
    page = 'players'
    players = database.get_players()
    shuffle(sponsorer)
    return render_template('players.html', page=page, title='Tilmeldte', players=players, drawn=draw, sponsorer=sponsorer)


@app.route('/vinder')
def banko():
    page = 'banko'
    shuffle(sponsorer)
    return render_template('banko.html', page=page, title="Banko!", sponsorer=sponsorer)


@app.route('/prizes')
def show_prizes():
    page = 'prizes'
    shuffle(sponsorer)
    return render_template('prizes.html', page=page, title="Præmier", sponsorer=sponsorer)


@app.route('/vindere')
def show_winners():
    page = 'winners'
    shuffle(sponsorer)
    return render_template('winners.html', page=page, title="Vindere", sponsorer=sponsorer)


if __name__ == '__main__':
    app.run()
