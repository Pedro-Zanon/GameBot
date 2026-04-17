import sqlite3

def init_db():

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    try:
        c.execute('DROP TABLE IF EXISTS test')
        c.execute('''
        CREATE TABLE test (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo      TEXT,
        preco       REAL,
        url         TEXT,
        created_at  DATETIME
        )
        ''')
    except Exception as e:
        print(e)

    conn.commit()
    conn.close()
    print("tabelas verificadas com sucesso!")

init_db()