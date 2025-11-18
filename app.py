from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "claveSegura"

mysql = MySQL(app)

# ---------- PÁGINA PRINCIPAL ----------
@app.route('/')
def index():
    return render_template('index.html')
# ---------- REGISTRO ----------
@app.route('/registrarse/<tipo>')
def registrarse(tipo):
    if tipo == "selector":
        return render_template("registrarse.html")

    if tipo not in ["conductor", "pasajero"]:
        return "Tipo de usuario no válido", 400

    return render_template("form_registro.html", tipo=tipo)


@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    contrasena = request.form['contraseña']
    matriculaEst = request.form['matriculaEst']
    numero_telefonico = request.form['numero_telefonico']
    matricula_coche = request.form['matricula_coche']
    tipo = request.form['tipo']

    if tipo == "pasajero":
        matricula_coche = None  # No se requiere para pasajeros

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO usuarios (nombre, apellido, correo, contraseña, matriculaEst, numero_telefonico, matricula_coche, tipo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (nombre, apellido, correo, contrasena, matriculaEst, numero_telefonico, matricula_coche, tipo))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


# ---------- INICIAR SESIÓN ----------
@app.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contraseña']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario, contraseña, tipo FROM usuarios WHERE correo=%s", (correo,))
        user = cur.fetchone()
        cur.close()

        if user and user[1] == contrasena:
            session['id_usuario'] = user[0]
            session['tipo'] = user[2]

            if user[2] == "conductor":
                return redirect(url_for('pageConductor'))
            else:
                return redirect(url_for('pagePasajero'))

        return "Usuario o contraseña incorrectos"

    return render_template('iniciarSesion.html')


# ---------- PÁGINAS PRINCIPALES ----------
@app.route('/pageConductor')
def pageConductor():
    if 'id_usuario' not in session:
        return redirect(url_for('iniciarSesion'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ruta WHERE id_usuario = %s", (session['id_usuario'],))
    rutas = cur.fetchall()
    cur.close()

    return render_template('pageConductor.html', rutas=rutas)


@app.route('/pagePasajero')
def pagePasajero():
    if 'id_usuario' not in session:
        return redirect(url_for('iniciarSesion'))

    return render_template('pagePasajero.html')


# ---------- AGREGAR RUTA SOLO DEL CONDUCTOR ----------
@app.route('/agregarRuta', methods=['GET', 'POST'])
def agregarRuta():
    if 'id_usuario' not in session:
        return redirect(url_for('iniciarSesion'))

    if session['tipo'] != 'conductor':
        return "Solo conductores pueden agregar rutas"

    if request.method == 'POST':
        calle = request.form['calle']
        punto_referencia = request.form['punto_referencia']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO ruta (calle, punto_referencia, id_usuario)
            VALUES (%s, %s, %s)
        """, (calle, punto_referencia, session['id_usuario']))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('pageConductor'))

    return render_template('agregarRuta.html')


# ----------- ELIMINAR Y EDITAR RUTA SOLO DEL PROPIETARIO ----------
@app.route('/eliminarRuta/<int:id>')
def eliminarRuta(id):
    if 'id_usuario' not in session:
        return redirect(url_for('iniciarSesion'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ruta WHERE id = %s AND id_usuario = %s", (id, session['id_usuario']))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('pageConductor'))


@app.route('/editarRuta/<int:id>')
def editarRuta(id):
    if 'id_usuario' not in session:
        return redirect(url_for('iniciarSesion'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ruta WHERE id = %s AND id_usuario=%s", (id, session['id_usuario']))
    ruta = cur.fetchone()
    cur.close()

    if not ruta:
        return "Ruta no encontrada o no autorizada", 404

    return render_template('editarRuta.html', ruta=ruta)


@app.route('/actualizarRuta/<int:id>', methods=['POST'])
def actualizarRuta(id):
    if 'id_usuario' not in session:
        return redirect(url_for('iniciarSesion'))

    calle = request.form['calle']
    referencia = request.form['punto_referencia']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE ruta SET calle=%s, punto_referencia=%s
        WHERE id=%s AND id_usuario=%s
    """, (calle, referencia, id, session['id_usuario']))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('pageConductor'))


# ---------- CERRAR SESIÓN ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
