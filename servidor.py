from crypt import methods
import webbrowser
from flask import Flask, request, render_template, redirect
from Usuarios import get_db, create_table
from funciones import create_table_productos, crear_empleado, deben, info_productos, get_usuario, table_productos_vendidos, creditos, registrarUsuario, create_table_empleados, create_table_local, create_carrito, limpiar_carrito, usuario, limpiar_usuario, actualizar_mes, actualizar_gastos
from datetime import datetime





app = Flask(__name__)

@app.route('/vitacora')
def vitacora():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    usuario = get_usuario()
    if usuario[0][1] == 'sorlenys':
        db = get_db()
        cur = db.cursor()
        cur.execute("select año, mes, dia, gasto from gastos")
        lista_gastos = cur.fetchall()
        cur.execute("select año, mes, dia, ventas from local")
        lista_ventas = cur.fetchall()
        db.close()
        vitacora = []
        for i in range(len(lista_ventas)):
            temporal = (f"{lista_ventas[i][2]}/{lista_ventas[i][1]}/{lista_ventas[i][0]}", lista_ventas[i][3], lista_gastos[i][3])
            vitacora.append(temporal)
        return render_template('vitacora.html', usuariodata = usuario, historial = vitacora)
    else:
        return redirect('/')
    

@app.route('/')
def index():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    creditos()
    actualizar_gastos()
    create_table()
    create_table_local()
    actualizar_mes()
    create_table_empleados()
    create_carrito()
    create_table_productos()

    db = get_db()
    cur = db.cursor()
    cur.execute("""create table if not exists pedidos(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        compra TEXT NOT NULL,
        valor REAL NOT NULL,
        llevar TEXT NOT NULL, 
        detalles TEXT NOT NULL)
        """)
    db.commit()
    db.close()
    

    db = get_db()
    cur = db.cursor()
    cur.execute("""create table if not exists inventario(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL)
        """)
    db.commit()
    db.close()

    table_productos_vendidos()

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

    usuario()
    db = get_db()
    cur = db.cursor()
    cur.execute("select usuario, nombre, sexo from usuario")
    preusuario = cur.fetchall()
    db.close()
    total = 0
    if preusuario != []:
        return redirect('/inicio')
    else:
        limpiar_usuario()
        usuario()
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    usuario()
    db = get_db()
    cursor = db.cursor()
    query = "SELECT user, password FROM usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    db.close()
    ingreso = False
    if request.method == 'POST':
        if 'ingresar' in request.form:
            user = request.form['username']
            password = request.form['password']
            for i in range(len(usuarios)):
                if user == usuarios[i][0] and password == usuarios[i][1]:
                    ingreso = True
                    break
            if ingreso == True:
                db = get_db()
                cur = db.cursor()
                cur.execute("""
                SELECT user, name, sexo from usuarios
                """)
                usuarios = cur.fetchall()
                for i in range(len(usuarios)):
                    if usuarios[i][0] == user:
                        usuari= usuarios[i]
                gusuario1 = usuari[0]
                gusuario2 = usuari[1]
                gusuario3 = usuari[2]
                usuario2 = [gusuario1, gusuario2, gusuario3]
                cur.execute("insert into usuario(usuario, nombre, sexo) values(?,?,?)", (gusuario1, gusuario2, gusuario3))
                db.commit()
                db.close()
                total = 0
                db = get_db()
                cur = db.cursor()
                query = "select producto, unidades, valor from carrito"
                cur.execute(query)
                carrito = cur.fetchall()
                for i in range(len(carrito)):
                    total += carrito[i][2]*carrito[i][1]
                db = get_db()
                cur = db.cursor()
                cur.execute("select año, mes, ventas from local")
                ventasmeses = cur.fetchall()
                ventas_mes = 0
                for i in ventasmeses:
                    if i[0] == año and i[1] == str(mes):
                        ventas_mes += i[2]
                db = get_db()
                cur = db.cursor()
                cur.execute("select año, mes, dia, ventas from local")
                venta_dia = cur.fetchall()
                db.close()
                venta_dia_hoy = 0
                for i in venta_dia:
                    if i[0] == año and i[1] == str(mes) and dia == i[2]:
                        venta_dia_hoy = i[3]
                db = get_db()
                cur = db.cursor()
                cur.execute("select nombre, valor from productos")
                productos1 = cur.fetchall()
                db.close()
                return render_template('inicio.html', usuariodata = usuario2, fecha = fe, productos = carrito, pagar = total, ventas = ventas_mes, ventas_hoy = venta_dia_hoy, lista_productos = productos1)
            else:
                return redirect('/login')
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def singup():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        create_table()
        user = request.form['username']
        password = request.form['password']
        name = request.form['name']
        sexo = request.form['sexo']
        if sexo not in ['masculino', 'Masculino', 'MASCULINO', 'femenino', 'Femenino', 'FEMENINO']:
            return redirect('/signup')
        if registrarUsuario(user, password, name, sexo) == True:
            db = get_db()
            cur = db.cursor()
            cur.execute("insert into empleados(nombre, ventas) values(?,?)", (name, 0))
            print(name)
            print('registrado en empleados')
            db.commit()
            db.close()
            print(name)
            return render_template('signup.html')
        else:
            return redirect('/signup')
    elif request.method == 'GET':
        preusuario = get_usuario()
        if preusuario[0][1] == 'sorlenys':
            db = get_db()
            cur = db.cursor()
            cur.execute("select nombre, valor from productos")
            productos1 = cur.fetchall()
            db.close()
            return render_template('signup.html', lista_productos = productos1)
        else:
            return redirect('/')

@app.route('/prueba', methods=['POST'])
def probar():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        mensaje_previo = request.form['mensaje']
        return render_template('edit.html', mensaje = mensaje_previo)
    else:
        return redirect('/')

@app.route('/edit')
def aja():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    return render_template('pruebas.html')


@app.route('/pedidos')
def pedidos():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    preusuario = get_usuario()
    usuario = preusuario[0]
    db = get_db()
    cur = db.cursor()
    cur.execute("select año, mes, ventas from local")
    ventasmeses = cur.fetchall()
    ventas_mes = 0
    for i in ventasmeses:
            if i[0] == año and i[1] == str(mes):
                ventas_mes += i[2]
    db = get_db()
    cur = db.cursor()
    cur.execute("select año, mes, dia, ventas from local")
    venta_dia = cur.fetchall()
    db.close()
    venta_dia_hoy = 0
    for i in venta_dia:
        if i[0] == año and i[1] == str(mes) and dia == i[2]:
            venta_dia_hoy = i[3]
    db = get_db()
    cur = db.cursor()
    cur.execute("select nombre, compra, valor, id, llevar, detalles from pedidos")
    lista_pedidos = cur.fetchall()
    lon = len(lista_pedidos)
    db.commit()
    db.close()
    return render_template('pedidos.html', usuariodata = usuario, fecha = fe, ventas = ventas_mes, ventas_hoy = venta_dia_hoy, mostrar_pedidos = lista_pedidos, largo = lon )

@app.route('/inicio' )
def inicio():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    creditos()
    actualizar_gastos()
    create_table()
    create_table_local()
    actualizar_mes()
    create_table_empleados()
    create_table_productos()
    limpiar_carrito()
    create_carrito()

    db = get_db()
    cur = db.cursor()
    cur.execute("""create table if not exists pedidos(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        compra TEXT NOT NULL,
        valor REAL NOT NULL,
        llevar TEXT NOT NULL, 
        detalles TEXT NOT NULL)
        """)
    db.commit()
    db.close()
    

    db = get_db()
    cur = db.cursor()
    cur.execute("""create table if not exists inventario(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL)
        """)
    db.commit()
    db.close()

    table_productos_vendidos()

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
    cur.execute("select usuario, nombre, sexo from usuario")
    preusuario = cur.fetchall()
    db.close()
    total = 0
    usuario = preusuario[0]
    db = get_db()
    cur = db.cursor()
    query = "select producto, unidades, valor from carrito"
    cur.execute(query)
    carrito = cur.fetchall()
    for i in range(len(carrito)):
        total += carrito[i][2]*carrito[i][1]
    db = get_db()
    cur = db.cursor()
    cur.execute("select año, mes, ventas from local")
    ventasmeses = cur.fetchall()
    ventas_mes = 0
    for i in ventasmeses:
            if i[0] == año and i[1] == str(mes):
                ventas_mes += i[2]
    db = get_db()
    cur = db.cursor()
    cur.execute("select año, mes, dia, ventas from local")
    venta_dia = cur.fetchall()
    db.close()
    venta_dia_hoy = 0
    for i in venta_dia:
        if i[0] == año and i[1] == str(mes) and dia == i[2]:
            venta_dia_hoy = i[3]
    db = get_db()
    cur = db.cursor()
    cur.execute("select nombre, valor from productos")
    productos1 = cur.fetchall()
    db.close()
    return render_template('inicio.html', usuariodata = usuario, fecha = fe, productos = carrito, pagar = total, ventas = ventas_mes, ventas_hoy = venta_dia_hoy, lista_productos = productos1)

@app.route('/cerrar_sesion')
def cerrar_sesion():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    limpiar_usuario()
    return redirect('/')

@app.route('/estadisticas')
def estadisticas():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    db = get_db()
    cur = db.cursor()
    cur.execute("select año, mes, ventas, dia from local")
    ventasmeses = cur.fetchall()
    db.close()
    ventas_mes = 0
    dias = []
    venta_dia = None
    dias_ventas = []
    gasto_dia = 0

    for i in ventasmeses:
        if i[0] == año and i[1] == str(mes) and i[3] == dia:
            print(i)
            venta_dia = i[2]
    
    db = get_db()
    cur = db.cursor()
    cur.execute("select año, mes, gasto, dia from gastos")
    gastosmeses = cur.fetchall()
    print(gastosmeses, 'gastos')
    db.close()

    for i in gastosmeses:
        print(i, 'pasé')
        if i[0] == año and i[1] == str(mes) and i[3] == dia:
            gasto_dia = i[2]
            print(gasto_dia, 'esto se gastó')

    for i in ventasmeses:
        if i[0] == año and i[1] == str(mes):
            dias.append(i)
            dias_ventas.append(i[2])
            ventas_mes += i[2]
    dias.sort()
    info_productos_mayor_y_menor = info_productos()
    lista = deben()
    db = get_db()
    cur = db.cursor()
    cur.execute("select nombre, ventas from empleados")
    empleados = cur.fetchall()
    print(empleados, 'empleados')
    db.commit()
    db.close()
    db = get_db()
    cur = db.cursor()
    cur.execute("select id, producto, cantidad from inventario")
    lista_inventario = cur.fetchall()
    if len(dias) > 0:
        dia_mayor = dias[len(dias)-1]
        dia_menor = dias[0]
    else:
        dia_mayor = (0,0,0,0)
        dia_menor = (0,0,0,0)
        venta_dia = 0

    return render_template('estadisticas.html', informe = ventas_mes, diaMas = dia_mayor, diaMenos = dia_menor, producto_menos = info_productos_mayor_y_menor[1], producto_mas = info_productos_mayor_y_menor[0], deben = lista, trabajadores = empleados, inventario_final = lista_inventario, venta_hoy = venta_dia, gasto = gasto_dia)

@app.route('/listaRentas', methods=['POST', 'GET'])
def listaRentas():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    create_carrito()
    db = get_db()
    cur = db.cursor()
    cur.execute("select usuario, nombre, sexo from usuario")
    preusuario = cur.fetchall()
    db.close()
    total = 0
    usuario = preusuario[0]
    if request.method == 'POST':
        producto = request.form['producto']
        unidades = request.form['unidades']
        db = get_db()
        cur = db.cursor()
        cur.execute("select nombre, valor from productos")
        productos1 = cur.fetchall()
        db.close()
        for i in productos1:
            if producto in i:
                valor = i[1]
                db = get_db()
                cur = db.cursor()
                cur.execute("insert into carrito(producto, unidades, valor) values(?,?,?)", (producto, unidades, valor))
                db.commit()
                db.close()
        db = get_db()
        cur = db.cursor()
        query = "select producto, unidades, valor from carrito"
        cur.execute(query)
        carrito = cur.fetchall()
        for i in range(len(carrito)):
            total += carrito[i][2]*carrito[i][1]

        db = get_db()
        cur = db.cursor()
        cur.execute("select año, mes, ventas from local")
        ventasmeses = cur.fetchall()
        db.close()
        ventas_mes = 0
        for i in ventasmeses:
            if i[0] == año and i[1] == str(mes):
                ventas_mes += i[2]
        db = get_db()
        cur = db.cursor()
        cur.execute("select año, mes, dia, ventas from local")
        venta_dia = cur.fetchall()
        db.close()
        venta_dia_hoy = 0
        for i in venta_dia:
            if i[0] == año and i[1] == str(mes) and dia == i[2]:
                venta_dia_hoy = i[3]

        return render_template('inicio.html', usuariodata = usuario, fecha = fe, productos = carrito, pagar = int(total), ventas = ventas_mes, ventas_hoy = venta_dia_hoy, lista_productos = productos1)
    else:
        return redirect('login.html')

@app.route('/listo_o_editar', methods=['POST'])
def listo():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        cur.execute("select nombre, compra, valor, id from pedidos")
        lista_pedidos = cur.fetchall()
        lon = len(lista_pedidos)
        db.commit()
        db.close()
        cliente = request.form['final']
        valor_pedido = request.form['valor_pedido']
        valor_pedido = float(valor_pedido)
        if 'listo' in request.form:
            for i in lista_pedidos:
                if i[0] == cliente:
                    db = get_db()
                    cur = db.cursor()
                    cur.execute(f"DELETE from pedidos where ID='{i[3]}'")
                    db.commit()
                    db.close()
            return redirect('/pedidos')
        elif 'editar' in request.form:
            db = get_db()
            cur = db.cursor()
            cur.execute('select año, mes, dia, ventas, id from local')
            local = cur.fetchall()
            db.close()
            
            for i in local:
                if i[0] == año and i[1] == str(mes) and i[2] == dia:
                    db = get_db()
                    cur = db.cursor()
                    print(valor_pedido)
                    print(i[4])
                    query2 = f"update local set año='{año}', mes='{mes}', dia ='{dia}', ventas='{i[3]-valor_pedido}' where id = '{i[4]}';"
                    cur.execute(query2)
                    db.commit()
                    db.close()
                    for i in lista_pedidos:
                        if i[0] == cliente:
                            db = get_db()
                            cur = db.cursor()
                            cur.execute(f"DELETE from pedidos where ID='{i[3]}'")
                            db.commit()
                            db.close()
                    return redirect('/')

    else:
        return redirect('/')

@app.route('/pagar', methods=['POST', 'GET'])
def pagar():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        cliente = request.form['cliente']
        pago = request.form['pago']
        total_pagar = request.form['total_pagar']
        print(total_pagar)
        llevar = request.form['llevar']
        detalles = request.form['detalles']

        db = get_db()
        cur = db.cursor()
        query = "select año, mes, dia from local"
        cur.execute(query)
        base = cur.fetchall()
        actualizar = True
        for i in base:
            if str(mes) == i[1] and año == i[0] and dia == i[2]:
                actualizar = False
        if actualizar == True:
            db = get_db()
            cur = db.cursor()
            query2 = "insert into local(año, mes, dia, ventas) values(?,?,?,?)"
            cur.execute(query2, (año, mes, dia, 0))
            db.commit()
            db.close()


        db = get_db()
        cur = db.cursor()
        query = "select producto, unidades, valor from carrito"
        cur.execute(query)
        lista = cur.fetchall()
        total = 0
        for i in lista:
            db = get_db()
            cur = db.cursor()
            table_productos_vendidos()
            query4 = "insert into productos_vendidos(nombre, cantidad) values(?,?)"
            cur.execute(query4, (i[0], i[1]))
            print(i[0], 'agregado')
            db.commit()
            db.close()
            total += i[1] * i[2]
            print(type(total))
        db.close()
        create_table_local()
        db = get_db()
        cur = db.cursor()
        cur.execute("select id, año, mes, dia, ventas from local")
        local = cur.fetchall()
        db.close()
        db = get_db()
        cur = db.cursor()
        for i in local:
            if i[1] == año and i[2] == str(mes) and i[3] == dia:
                query2 = f"update local set año='{año}', mes='{mes}', dia ='{dia}', ventas='{i[4]+total}' where id = '{i[0]}';"
                cur.execute(query2)
                db.commit()
                db.close()
                limpiar_carrito()
                create_carrito()
        creditos()
        print(pago, 'a credito?')
        db = get_db()
        cur = db.cursor()
        cur.execute("select usuario, nombre, sexo from usuario")
        preusuario = cur.fetchall()
        db.close()
        db = get_db()
        cur = db.cursor()
        cur.execute("select nombre, ventas, id from empleados")
        empleados = cur.fetchall()
        for i in empleados:
            if i[0] == preusuario[0][1]:
                cur.execute(f"update empleados set nombre='{i[0]}', ventas='{total+i[1]}' where id='{i[2]}';")
                db.commit()
                db.close()
                break
        if pago in ['si', 'sí', 'SI', 'SÍ', 'Si', 'sI']:
            today = datetime.now()
            año = today.year
            mes = today.month
            dia = today.day
            fe = f'{dia}/{mes}/{año}'
            db = get_db()
            cur = db.cursor()
            query = "select cliente, debe, id from creditos"
            cur.execute(query)
            lista_todos = cur.fetchall()
            db.close()
            db = get_db()
            cur = db.cursor()
            registro = False
            db = get_db()
            cur = db.cursor()
            query = "select producto, unidades, valor from carrito"
            cur.execute(query)
            carrito = cur.fetchall()
            for i in carrito:
                total += i[2]*i[1]
                print(type(total))

            for i in range(len(lista_todos)):
                if cliente == lista_todos[i][0]:
                    total_pagar_final = lista_todos[i][1] + total
                    cur.execute(f"update creditos set cliente = '{cliente}', debe = '{total_pagar_final}' where id='{lista_todos[i][2]}';")
                    db.commit()
                    db.close()
                    registro = True
                    break
            if registro == False:
                creditos()
                db = get_db()
                cur = db.cursor()
                query3 = "insert into creditos(cliente, debe) values(?,?)"
                cur.execute(query3, (cliente, total_pagar))
                db.commit()
                db.close()
        db = get_db()
        cur = db.cursor()
        cur.execute("""create table if not exists pedidos(
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            compra TEXT NOT NULL,
            valor REAL NOT NULL,
            llevar TEXT NOT NULL, 
            detalles TEXT NOT NULL)
            """)
        db.commit()
        db.close()
        compra = ""
        vueltas = 0
        for i in lista:
            if vueltas == 0:
                if i[1] != 1:
                    compra += f"{i[0]} X{i[1]}"
                else:
                    compra += f"{i[0]}"
            else:
                if i[1] != 1:
                    compra += f", {i[0]} X{i[1]}"
                else:
                    compra += f", {i[0]}"
            vueltas += 1
        db = get_db()
        cur = db.cursor()
        cur.execute("insert into pedidos(nombre, compra, valor, llevar, detalles) values(?,?,?,?,?)", (cliente, compra, total, llevar, detalles))
        db.commit()
        db.close()
        db = get_db()
        cur = db.cursor()
        cur.execute("select id, producto, cantidad from inventario")
        lista_inventario = cur.fetchall()
        for i in lista_inventario:
            for a in lista:
                if i[1] == a[0]:
                    prod_final = int(a[1])
                    db = get_db()
                    cur = db.cursor()
                    cur.execute(f"update inventario set producto='{i[1]}', cantidad='{i[2]-prod_final}' where id='{i[0]}'")
                    db.commit()
                    db.close()
        return render_template('imprimir.html', ticket = lista, pt = total, name = cliente, details = detalles)

    else:
        return redirect('/')

@app.route('/borrar', methods=['POST'])
def borrar():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        cliente = request.form['cliente']
        db = get_db()
        cur = db.cursor()
        cur.execute("select cliente, id from creditos")
        lista = cur.fetchall()
        db.close()
        db = get_db()
        cur = db.cursor()
        for i in lista:
            if cliente == i[0]:
                cur.execute(f"DELETE from creditos where id='{i[1]}'")
                db.commit()
                db.close()
                break
    return redirect('/estadisticas')


@app.route('/reiniciar_carrito')
def reiniciar():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    limpiar_carrito()
    create_carrito()
    return redirect('/')

@app.route('/reiniciar_borrar', methods=['POST'])
def r_b():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        trabajador = request.form['trabajador']
        if 'eliminar' in request.form:
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
                if i[0] == trabajador:
                    db = get_db()
                    cur = db.cursor()
                    cur.execute(f"DELETE from empleados where id='{i[1]}'")
                    print('eliminado de empleados')
                    db.commit()
                    db.close()
                    for a in lista2:
                        print(a[0])
                        if a[0] == trabajador:
                            db = get_db()
                            cur = db.cursor()
                            cur.execute(f"DELETE from usuarios where id='{a[1]}'")
                            print('eliminado de usuarios')
                            db.commit()
                            db.close()
        elif 'reiniciar' in request.form:
            db = get_db()
            cur = db.cursor()
            cur.execute("select nombre, id from empleados")
            lista = cur.fetchall()
            db.commit()
            db.close()
            for i in lista:
                if i[0] == trabajador:
                    db = get_db()
                    cur = db.cursor()
                    cur.execute(f"update empleados set nombre = '{i[0]}', ventas = '{0}' where id='{i[1]}';")
                    db.commit()
                    db.close()
    return redirect('/estadisticas')

@app.route('/gasto', methods=['POST'])
def gastos():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        motivo = request.form['motivo_gasto']
        valor_inicial = request.form['valor_gasto']
        gasto = float(valor_inicial)/1000
        db = get_db()
        cur = db.cursor()
        cur.execute("select id, año, mes, dia, gasto from gastos")
        local = cur.fetchall()
        print(local, 'revisar')
        db.close()
        db = get_db()
        cur = db.cursor()
        actualizar = False
        for i in local:
            if i[1] == año and i[2] == mes and i[3] == dia:
                actualizar = True
        if actualizar == True:
            query2 = f"update gastos set año='{i[1]}', mes='{i[2]}', dia ='{i[3]}', gasto='{i[4]+gasto}' where id = '{i[0]}';"
        else:
            query2 = f"insert into gastos(año, mes, dia, gasto) values(?,?,?,?)"
        cur.execute(query2, (año,mes,dia,gasto))
        db.commit()
        db.close()
        return redirect('/signup')

@app.route('/inventario', methods=['POST'])
def inventario():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'
    if request.method == 'POST':
        producto = request.form['producto']
        unidades = request.form['unidades_compra']

        db = get_db()
        cur = db.cursor()
        cur.execute("select id, producto, cantidad from inventario")
        lista = cur.fetchall()
        registrar = True
        registro = None
        for i in lista:
            if producto == i[1]:
                registrar = False
                registro = i
                break
        
        if registrar == False:
                prod_final = int(unidades)
                db = get_db()
                cur = db.cursor()
                cur.execute(f"update inventario set producto='{registro[1]}', cantidad='{registro[2]+prod_final}' where id='{registro[0]}'")
                db.commit()
                db.close()

        else:
            prod_final = int(unidades)
            db = get_db()
            cur = db.cursor()
            cur.execute("insert into inventario(producto, cantidad) values(?,?)", (producto, prod_final))
            db.commit()
            db.close()
        return redirect('/signup')
    else:
        return redirect('/')

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['producto']
        valor = request.form['valor_producto']
        db = get_db()
        cur = db.cursor()
        query= "insert into productos(nombre, valor) values(?,?)"
        valorf = int(valor)/1000
        cur.execute(query, (nombre, valorf))
        print(f'Registrado {nombre} con un precio de {valorf}')
        db.commit()
        db.close()
        return redirect('/inicio')

if __name__ == '__main__':
    create_table()
    app.run(debug = True)