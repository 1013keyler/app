from Usuarios import get_db, create_table
from datetime import datetime

def actualizar_gastos():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    db = get_db()
    cur = db.cursor()
    cur.execute("""create table if not exists gastos(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        año INTEGER NOT NULL,
        mes TEXT NOT NULL,
        dia INTEGER NOT NULL,
        gasto REAL NOT NULL)
        """)
    db.commit()
    db.close()
    db = get_db()
    cur = db.cursor()
    cur.execute("select id, año, mes, dia, gasto from gastos")
    local = cur.fetchall()
    print(local, 'revisar')
    db.close()
    db = get_db()
    cur = db.cursor()
    actualizar = True
    for i in local:
        if i[1] == año and i[2] == mes and i[3] == dia:
            actualizar = False
            break
    if actualizar == True:
        query2 = f"insert into gastos(año, mes, dia, gasto) values(?,?,?,?)"
        cur.execute(query2, (año,mes,dia,0))
        db.commit()
        db.close()

def registrarUsuario(user, password, name, sexo):
    today = datetime.now()
    año = today.year
    mes_n = today.month
    dia = today.day
    fe = f'{dia}/{mes_n}/{año}'
    create_table()
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT user FROM usuarios"
    cursor.execute(statement)
    usuarios = cursor.fetchall()
    registro = True
    for i in range(len(usuarios)):
        if user == usuarios[i][0]:
            registro = False
            break
    if registro == True: 
        query = "INSERT INTO usuarios(user, password, name, sexo) VALUES(?,?,?,?)"
        cursor.execute(query, (user, password, name, sexo))
        db.commit()
        db.close()
    return registro

def crear_empleado(nombre):
	db = get_db()
	cur = db.cursor()
	cur.execute(f"insert into empleados(nombre, ventas) values(?,?)", (nombre, 0))
	db.commit()
	db.close()

def create_table_empleados():
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS empleados(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ventas INTEGER NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def create_table_local():
    today = datetime.now()
    año = today.year
    mes_n = today.month
    dia = today.day
    fe = f'{dia}/{mes_n}/{año}'
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS local(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    mes TEXT NOT NULL,
    dia INTEGER NOT NULL,
    ventas REAL NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def create_table_productos():
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS productos(
    nombre TEXT NOT NULL,
    valor REAL NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def create_carrito():
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS carrito(
    producto TEXT NOT NULL,
    unidades INTEGER NOT NULL,
    valor REAL NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def limpiar_carrito():
    db = get_db()
    query = """
    DROP TABLE IF EXISTS carrito
    """
    db.execute(query)
    db.commit()
    db.close()

def usuario():
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS usuario(
    usuario TEXT NOT NULL,
    nombre TEXT NOT NULL,
    sexo TEXT NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def limpiar_usuario():
    db = get_db()
    query = """
    DROP TABLE IF EXISTS usuario
    """
    db.execute(query)
    db.commit()
    db.close()

def get_usuario():
    db = get_db()
    cur = db.cursor()
    cur.execute("select usuario, nombre, sexo from usuario")
    preusuario = cur.fetchall()
    db.close()
    return preusuario

def actualizar_mes():
    today = datetime.now()
    año = today.year
    mes_n = today.month
    dia = today.day
    fe = f'{dia}/{mes_n}/{año}'
    db = get_db()
    cur = db.cursor()
    db.commit()
    db.close()
    db = get_db()
    cur = db.cursor()
    query = "select año, mes, dia from local"
    cur.execute(query)
    base = cur.fetchall()
    actualizar = True
    for i in base:
        if str(mes_n) == i[1] and año == i[0] and dia == i[2]:
            print(f'mes {i[1]} año {i[0]}')
            actualizar = False
            break
    if actualizar == True:
        db = get_db()
        cur = db.cursor()
        query2 = "insert into local(año, mes, dia, ventas) values(?,?,?,?)"
        cur.execute(query2, (año, mes_n, dia, 0))
        db.commit()
        db.close()


def creditos():
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS creditos(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    debe REAL NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def table_productos_vendidos():
    db = get_db()
    query = """
    CREATE TABLE IF NOT EXISTS productos_vendidos(
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL)
    """
    db.execute(query)
    db.commit()
    db.close()

def deben():
    db = get_db()
    cur = db.cursor()
    query = "select cliente, debe from creditos"
    cur.execute(query)
    lista = cur.fetchall()
    print(lista)
    db.close()
    return lista

def info_productos():
    db = get_db()
    cur = db.cursor()
    query = "select nombre, cantidad from productos_vendidos"
    cur.execute(query)

    productos_vendidos = cur.fetchall()
    db.close()

    productos_mas_menos = []
    cantidad_producto = []

    for i in productos_vendidos:
        if i[0] in productos_mas_menos:
            indice = productos_mas_menos.index(i[0])
            cantidad_producto[indice] += i[1]
        else:
            productos_mas_menos.append(i[0])
            cantidad_producto.append(i[1])

    if len(cantidad_producto) > 0:
        mayori = cantidad_producto.index(max(cantidad_producto))
        minimoi = cantidad_producto.index(min(cantidad_producto))
        mayor = (productos_mas_menos[mayori], cantidad_producto[mayori])
        menor = (productos_mas_menos[minimoi], cantidad_producto[minimoi])
        menos_y_mas = [mayor, menor]
    else:
        menos_y_mas = [('SIN REGISTROS', 'SIN REGISTROS'),('SIN REGISTROS', 'SIN REGISTROS')]
    return menos_y_mas

def eliminar_empleado(name):
	db = get_db()
	cur = db.cursor()
	cur.execute("select nombre, id from empleados")
	lista = cur.fetchall()
	db.commit()
	db.close()

	db = get_db()
	cur = db.cursor()
	cur.execute("select name, id from usuarios")
	lista2 = cur.fetchall()
	db.commit()
	db.close()
    
	for i in lista:
		if i[0] == name:
			db = get_db()
			cur = db.cursor()
			cur.execute(f"DELETE from empleados where id='{i[1]}'")
			db.commit()
			db.close()
			for a in lista2:
				if a[0] == name:
					db = get_db()
					cur = db.cursor()
					cur.execute(f"DELETE from usuarios where id='{a[1]}'")
					db.commit()
					db.close()


