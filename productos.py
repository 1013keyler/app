from funciones import create_table_productos, get_db, limpiar_carrito

def registrar_producto(nombre, valor):
    db = get_db()
    cur = db.cursor()
    query= "insert into productos(nombre, valor) values(?,?)"
    valorf = valor/1000
    cur.execute(query, (nombre, valorf))
    print(f'Registrado {nombre} con un precio de {valorf}')
    db.commit()
    db.close()

while True:
    nombre = input('Nombre del producto: ')
    valor = int(input('Valor: '))
    registrar_producto(nombre, valor)
    