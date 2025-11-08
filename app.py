from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM conductor")
    conductores = cur.fetchall()

    cur.execute("SELECT * FROM pasajero")
    pasajeros = cur.fetchall()

    cur.close()
    return render_template('index.html', conductores=conductores, pasajeros=pasajeros)

@app.route('/registro_conductor', methods=['GET'])
def registro_conductor():
    return render_template('registro_conductor.html')


    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO conductor (Nombre, Apellido, matricula, emailInst, matriculaCoche)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, apellido, matricula, email, matricula_coche))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/guardar_conductor', methods=['POST'])
def guardar_conductor():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    matricula = request.form['matricula']
    email = request.form['email']
    matricula_coche = request.form['matricula_coche']

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO conductor (Nombre, Apellido, matricula, emailInst, matriculaCoche)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, apellido, matricula, email, matricula_coche))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/registro_pasajero', methods=['GET'])
def registro_pasajero():
    return render_template('registro_pasajero.html')

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO pasajero (Nombre, Apellido, matricula, emailInst)
        VALUES (%s, %s, %s, %s)
    """, (nombre, apellido, matricula, email))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/guardar_pasajero', methods=['POST'])
def guardar_pasajero():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    matricula = request.form['matricula']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO pasajero (Nombre, Apellido, matricula, emailInst)
        VALUES (%s, %s, %s, %s)
    """, (nombre, apellido, matricula, email))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
