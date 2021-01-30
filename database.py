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


if __name__ == '__main__':
    print(get_players())