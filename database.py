import sqlite3
from random import choice

player_db = 'db/players.sqlite3'


def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def get_players(inputName=None, inputSurname=None, gameweek=None):
    conn = create_connection(player_db)
    if inputName and inputSurname and gameweek:
        sql = 'select * from players WHERE inputName LIKE ? and inputSurname LIKE ? and gameweek LIKE ? ORDER BY inputName, inputSurname'
        cur = conn.cursor()
        cur.execute(sql, (inputName, inputSurname, gameweek))
    elif gameweek:
        sql = 'select * from players WHERE gameweek LIKE ? ORDER BY inputName, inputSurname'
        cur = conn.cursor()
        cur.execute(sql, (gameweek,))
    else:
        sql = 'select * from players ORDER BY inputName, inputSurname'
        cur = conn.cursor()
        cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def add_registration(fields):
    conn = create_connection(player_db)
    sql = "INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))"
    cur = conn.cursor()
    """inputName, inputSurname, inputRow1_0, inputRow1_1, inputRow1_2, inputRow1_3, inputRow1_4, inputRow2_0, inputRow2_1, inputRow2_2, inputRow2_3, inputRow2_4, inputRow3_0, inputRow3_1, inputRow3_2, inputRow3_3, inputRow3_4, gameweek, created"""
    cur.execute(sql, (fields))
    conn.commit()
    return cur.lastrowid


def banko_in_row(row, drawn):
    counter = 0
    for num in row:
        if num in drawn:
            counter += 1
    return counter == 5


if __name__ == '__main__':
    uge8 = [
        [37, 51, 65, 87, 86, 15, 82, 13, 56, 57], [26, 49, 30, 71, 12, 74, 52, 33, 77, 44],
        [63, 34, 75, 9, 31, 38, 39, 17, 22, 80],   # Rie på nummer 63
        [32, 2, 84, 72, 88, 67, 41, 78, 81, 73],
        [64, 90, 1, 7, 16, 85, 6, 27, 43, 69],
        [46, 10, 66, 76, 79, 60, 3, 5, 18, 50],  # Bente på 3
        [19, 54, 25, 8, 83, 89, 29, 4, 68, 62],
        [48, 24, 11, 40, 28, 14, 53, 70, 36, 47],  # Minou på nummer 24
        [45, 58, 21, 61, 42, 55, 35, 20, 23, 59]]

    uge7 = [[17, 24, 37, 75, 27, 33, 20, 88, 57, 62],
            [52, 81, 77, 87, 41, 80, 89, 76, 1, 67],
            [11, 39, 44, 60, 3, 66, 40, 78, 73, 31],  # Christian Palle på  nummer 3
            [13, 65, 50, 84, 35, 71, 7, 34, 69, 61],
            [56, 14, 58, 55, 9, 79, 10, 48, 21, 6],
            [2, 8, 12, 46, 29, 18, 74, 51, 83, 53],  # Sonny på nummer 74
            [25, 47, 45, 90, 63, 32, 49, 36, 68, 42],  # Hedi på nummer 90
            [30, 43, 22, 82, 64, 16, 5, 70, 72, 85],
            [38, 26, 15, 19, 4, 86, 54, 28, 23, 59]]

    draws = uge7

    draw = draws[0] + draws[1] + draws[2] + draws[3] + draws[4] + draws[5] #+ draws[6] #+ draws[7] #+ draws[8]
    players = get_players(gameweek='uge7')
    print(f'Trukket: {draw}')
    print()
    for player in players:
        row1 = player[2:7]
        row2 = player[7:12]
        row3 = player[12:17]
        rows = [row1, row2, row3]
        wins = 0
        for row in rows:
            if banko_in_row(row, draw):
                wins += 1
                if wins == 2:
                    print(f'{player[0]} {player[1]}: {rows}')
