from funciones import get_db, limpiar_carrito, create_table_local

db = get_db()
cur = db.cursor()
cur.execute("drop table if exists local")
cur.execute("drop table if exists creditos")
cur.execute("drop table if exists productos_vendidos")
cur.execute("drop table if exists inventario")
cur.execute("drop table if exists gastos")

cur.execute("""
    CREATE TABLE IF NOT EXISTS local(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    mes TEXT NOT NULL,
    dia INTEGER NOT NULL,
    ventas REAL NOT NULL)
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS creditos(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    debe REAL NOT NULL)
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS productos_vendidos(
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL)
    """)

cur.execute("""create table if not exists inventario(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL)
        """)

cur.execute("""create table if not exists gastos(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        año INTEGER NOT NULL,
        mes TEXT NOT NULL,
        dia INTEGER NOT NULL,
        gasto REAL NOT NULL)
        """)
db.commit()
db.close()