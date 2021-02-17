from flask import Flask, render_template, request, redirect, url_for
from random import choice, shuffle
import database

app = Flask(__name__)
app.secret_key = b"dette er en hemmelig streng"
app.url_map.strict_slashes = False
WTF_CSRF_SECRET_KEY = "a random string"

draws = [[17, 24, 37, 75, 27, 33, 20, 88, 57, 62],
         [52, 81, 77, 87, 41, 80, 89, 76, 1, 67], # Mandag
         [11, 39, 44, 60, 3, 66, 40, 78, 73, 31],  # June på 3, (Christian Palle på  nummer 40,  Pernille på 31,)
         [13, 65, 50, 84, 35, 71, 7, 34, 69, 61], # Onsdag
         [56, 14, 58, 55, 9, 79, 10, 48, 21, 6],  # Torsdag
         [2, 8, 12, 46, 29, 18, 74, 51, 83, 53],  # Sonny på nummer 74
         [25, 47, 45, 90, 63, 32, 49, 36, 68, 42],  # Hedi på nummer 90
         [30, 43, 22, 82, 64, 16, 5, 70, 72, 85],  # Søndag
         [38, 26, 15, 19, 4, 86, 54, 28, 23, 59]]

draw = draws[0] + draws[1] + draws[2] + draws[3] + draws[4] #+ draw[s5] #+ draws[6] #+ draws[7]
latest_draw = draws[4]

sponsorer = [
    ['FairIT.png', 'Fair IT A/S'],
    ['danbolig.png', 'Danbolig Holbæk'],
    ['liljehoj.jpg', 'Liljehøj'],
    ['lykkegard.png', 'Lykkegard'],
    ['massorskolen.png', 'Massørskolen-Fyn'],
    ['parasport.png', 'Parasport Danmark'],
    ['revisorgaarden.png', 'RevisorGården Holbæk'],
    ['slagterknabstrup.png', 'Slageren i Knabstrup'],
    ['sparekassen.png', 'Sparekassen Sjælland-Fyn'],
    ['superbrugsenasnaes.png', 'Superbrugsen Asnæs'],
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
        if fields.get('gameweek', None) == 'uge7':
            errors.append('Der kan ikke længere registreres plader for uge 7.')
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
    return render_template('register.html', page=page, title="Deltag!", rows=rows, name=name, gameweek=gameweek,
                           surname=surname, errors=errors, sponsorer=sponsorer)


@app.route('/tilmeldte')
def show_players():
    page = 'players'
    players = database.get_players()
    shuffle(sponsorer)
    return render_template('players.html', page=page, title='Tilmeldte', players=players, drawn=draw,
                           sponsorer=sponsorer)


@app.route('/vinder')
def banko():
    page = 'banko'
    shuffle(sponsorer)
    return render_template('banko.html', page=page, title="Banko!", sponsorer=sponsorer)


@app.route('/prizes')
@app.route('/vindere')
def show_winners():
    page = 'winners'
    shuffle(sponsorer)
    return render_template('winners.html', page=page, title="Vindere", sponsorer=sponsorer)


if __name__ == '__main__':
    app.run()
