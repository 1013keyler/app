from flask import Flask, render_template, request, redirect
from config import config
from Usuarios import get_db, create_table
from funciones import registrarUsuario
from datetime import datetime

today = datetime.now()
año = today.year
mes = today.month
dia = today.day
fecha = 'f{dia}/{mes}/{año}'

app = Flask('Administrado de ventas')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        create_table()
        user = request.form['username']
        password = request.form['password']
        name = request.form['name']
        if registrarUsuario(user, password, name) == True:
            return render_template('inicio.html')
        else:
            return redirect('/signup')
    elif request.method == 'GET':
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
            print(f'Usuario: {user} Clave: {password}')
            print(usuarios)
            for i in range(len(usuarios)):
                if user == usuarios[i][0] and password == usuarios[i][1]:
                    ingreso = True
                    break
            print(ingreso)
            if ingreso == True:
                db = get_db()
                db.execute("""CREATE TABLE IF NOT EXISTS registros(
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo TEXT NOT NULL,
                dias INTERGER NOT NULL,
                nombre TEXT NOT NULL,
                documento INTERGER NOT NULL,
                horar TEXT NOT NULL,
                horae TEXT NOT NULL,
                diar TEXT NOT NULL,
                diae TEXT NOT NULL,
                monto INTERGER NOT NULL
                )
                """)
                cur = db.cursor()
                cur.execute("SELECT id, vehiculo, dias, nombre, documento, horar, horae, diar, diae, monto FROM registros ORDER BY id DESC")
                data = cur.fetchall()
                db.close()
                print(data)
                dateh = datetime.now().strftime("%H:%M:%S")
                datef = datetime.now().strftime("%d %B, %Y")
                return render_template('inicio.html', listaRentas = data, hora = dateh, fecha = datef)
            else:
                return redirect('/login')
        elif 'registrar' in request.form:
            return redirect('/signup')
    elif request.method == 'GET':
        return render_template('login.html')


        
@app.route('/listaRentas', methods=['POST', 'GET'])
def listaRentas():
    if request.method == 'POST':
        vehiculo = request.form['vehiculo']
        dias = request.form['dias']
        name = request.form['name']
        documento = request.form['documento']
        horar = request.form['horar']
        horae = request.form['horae']
        diar = request.form['diar']
        diae = request.form['diae']
        monto = request.form['monto']
        db = get_db()
        db.execute("""CREATE TABLE IF NOT EXISTS registros(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        vehiculo TEXT NOT NULL,
        dias INTERGER NOT NULL,
        nombre TEXT NOT NULL,
        documento INTERGER NOT NULL,
        horar TEXT NOT NULL,
        horae TEXT NOT NULL,
        diar TEXT NOT NULL,
        diae TEXT NOT NULL,
        monto INTERGER NOT NULL
        )
        """)
        cur = db.cursor()
        db.execute("INSERT INTO registros(vehiculo, dias, nombre, documento, horar, horae, diar, diae, monto) VALUES(?,?,?,?,?,?,?,?,?)", (vehiculo, dias, name, documento, horar, horae, diar, diae, monto))
        db.commit()
        cur.execute("SELECT id, vehiculo, dias, nombre, documento, horar, horae, diar, diae, monto FROM registros ORDER BY id DESC")
        data = cur.fetchall()
        db.close()
        print(data)
        dateh = datetime.now().strftime("%H:%M:%S")
        datef = datetime.now().strftime("%d %B, %Y")
        return render_template('inicio.html', listaRentas = data, hora = dateh, fecha = datef)
    else:
        return redirect('login')

@app.route('/ventas', methods=['POST', 'GET'])
def mostrarVentas():
    bd = get_db()
    cur = bd.cursor()
    query = "SELECT * FROM registros"
    cur.execute(query)
    lista = cur.fetchall()
    ganacias = 0
    NlistaRentas = 0
    for i in range(len(lista)):
        ganacias += lista[i][len(lista)-1]
        NlistaRentas = i + 1
    return render_template('ventas.html', listaRentas = lista, gananciasT = ganacias, cantidadlistaRentas = NlistaRentas)

@app.route('/edicionExcitosa', methods=['POST', 'GET'])
def editar():
    if request.method == 'POST':
        identificador = request.form['id']
        vehiculo = request.form['vehiculo']
        dias = request.form['dias']
        name = request.form['name']
        documento = request.form['documento']
        horar = request.form['horar']
        horae = request.form['horae']
        diar = request.form['diar']
        diae = request.form['diae']
        monto = request.form['monto']
        db = get_db()
        cur = db.cursor()
        query = f"update registros set producto='{vehiculo}', unidades='{dias}', nombre='{name}', documento='{documento}', horar = '{horar}', horae = '{horae}', diar = '{diar}', diae = '{diae}', monto = '{monto}'  where id='{identificador}';"
        cur.execute(query)
        db.commit()
        cur.execute("SELECT id, vehiculo, dias, nombre, documento, horar, horae, diar, diae, monto FROM registros ORDER BY id DESC")
        registro = cur.fetchall()
        db.close()
        return render_template('inicio.html', listaRentas=registro)

@app.route('/edicion', methods=['POST', 'GET'])
def editarOeliminar():
    if request.method == 'POST':
        identificador = request.form['id']
        print('hasta')
        vehiculo = request.form['vehiculo']
        dias = request.form['dias']
        name = request.form['name']
        documento = request.form['documento']
        horar = request.form['horar']
        horae = request.form['horae']
        diar = request.form['diar']
        diae = request.form['diae']
        monto = request.form['monto']
        registro = [identificador, vehiculo, dias, name, documento, horar, horae, diar, diae, monto]
        if 'editar' in request.form:
            return render_template('edit.html', editar = registro)
        elif 'eliminar' in request.form:
            db = get_db()
            cur = db.cursor()
            cur.execute("DELETE from registros where ID="+identificador)
            db.commit()
            cur.execute("SELECT id, vehiculo, dias, nombre, documento, horar, horae, diar, diae, monto FROM registros ORDER BY id DESC")
            registro = cur.fetchall()
            db.close()
            return render_template('inicio.html', listaRentas=registro)
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()