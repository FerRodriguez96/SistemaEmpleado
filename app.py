from logging import debug
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory

from datetime import datetime

import os


app= Flask(__name__)
app.secret_key="Fernando"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

Carpeta =os.path.join('uploads')
app.config['Carpeta']=Carpeta

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['Carpeta'],nombreFoto)

@app.route('/')
def index():

    sql ="SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    conn.commit()

    return render_template('empleados/index.html', empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("SELECT foto FROM empleados WHERE id=%s",id)
    fila=cursor.fetchall()

    os.remove(os.path.join(app.config['Carpeta'],fila[0][0]))
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()

    return render_template('empleados/edit.html',empleados=empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]

    id=request.form['txtID']

    sql ="UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"

    datos =(_nombre,_correo,id)

    conn = mysql.connect()
    cursor= conn.cursor()

    now = datetime.now()
    tiempo= now.strftime("%Y%H%M$S")

    if _foto.filename!="":
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT foto FROM empleados WHERE id=%s",id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['Carpeta'],fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()


    cursor.execute(sql,datos)

    conn.commit()

    return redirect('/')

@app.route('/store', methods=['POST'])
def storage():
    try:
        _nombre = request.form['txtNombre']
        _correo = request.form['txtCorreo']
        _foto = request.files['txtFoto']
    except:
        flash('Los datos ingresados no son correctos')
        return redirect (url_for('create'))

    now = datetime.now()
    tiempo= now.strftime("%Y%H%M$S")
    
    if _foto.filename!="":
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    datos =(_nombre,_correo,nuevoNombreFoto)

    sql ="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    conn = mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect ('/')

if __name__ == '__main__':
    app.run(debug=True)