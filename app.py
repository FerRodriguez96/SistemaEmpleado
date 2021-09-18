from logging import debug
from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL


app= Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


@app.route('/')
def index():

   

    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():

    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]

    datos =(_nombre,_correo,_foto.filename)
    sql ="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    conn = mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(debug=True)