@app.route('/pagar')
def pagar():

    cliente = request.form['cliente']
    pago = request.form['pago']
    pagar = request.form['total_pagar']
    print(cliente, pago, pagar)

    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{dia}/{mes}/{año}'

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
        total += (i[1] * i[2])
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
            limpiar_carrito()
            create_carrito()
    db.close()
    creditos
    if pago in ['si, sí, SI, SÍ, Si sI']:
        today = datetime.now()
        año = today.year
        mes = today.month
        dia = today.day
        fe = f'{dia}/{mes}/{año}'
        creditos()
        db = get_db()
        cur = db.cursor()
        query3 = "insert into creditos(cliente, fecha, debe) values(?,?,?)"
        cur.execute(query3, (cliente, fe, total_pagar))
        db.commit()
        db.close()
    return redirect('/')