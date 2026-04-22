import sqlite3

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jogos'")
    if not c.fetchone():
        c.execute('''
        CREATE TABLE jogos (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            nome             TEXT,
            preco            TEXT,
            desconto         TEXT,
            avaliacao        TEXT,
            genero           TEXT,
            link             TEXT,
            tipo             TEXT,
            created_at       DATETIME
        )
        ''')
        print("Tabela 'jogos' criada com sucesso!")
    else:
        print("Tabela 'jogos' ja existe!")

    conn.commit()
    conn.close()

init_db()