import sqlite3 as sql

def get_db():
    db = sql.connect('basedatos.db')
    return db
    
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    sexo TEXT NOT NULL
    )
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()
