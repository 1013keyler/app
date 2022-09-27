from funciones import get_db, create_table_empleados

db = get_db()
cur = db.cursor()
cur.execute("drop table if exists empleados")
db.commit()
db.close()

create_table_empleados()

def crear_empleado(nombre):
	db = get_db()
	cur = db.cursor()
	cur.execute(f"insert into empleados(nombre, ventas) values(?,?)", (nombre, 0))
	db.commit()
	db.close()

def eliminar_empleado(name):
	db = get_db()
	cur = db.cursor()
	cur.execute("select nombre, id from empleados")
	lista = cur.fetchall()
	db.commit()
	db.close()

	db = get_db()
	cur = db.cursor()
	cur.execute("select nombre, id from usuarios")
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

def reiniciar_empleado(name):
	db = get_db()
	cur = db.cursor()
	cur.execute("select nombre, id from empleados")
	lista = cur.fetchall()
	db.commit()
	db.close()
	for i in lista:
		if i[0] == name:
			db = get_db()
			cur = db.cursor()
			cur.execute(f"update empleados set nombre = '{name}', ventas = '{0}' where id='{i[1]}';")
			db.commit()
			db.close()