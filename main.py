from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventoryflask'

mysql = MySQL(app)

@app.route('/inventoryflask/', methods=['GET', 'POST'])
def login():
    msg = 'Error en el sistema'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return 'Logeo concedido'
        else:
            msg = 'Datos incorrectos'
    return render_template('index.html', msg='')

@app.route('/inventoryflask/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/inventoryflask/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Existe ya una cuenta con ese nombre'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'E-Mail invalido'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'El usuario solo debe contener caracteres validos'
        elif not username or not password or not email:
            msg = 'Porfavor rellene de forma correcta la forma'
        else:
            cursor.execute('INSERT INTO admin VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'Esta registrado en la base de datos'
    elif request.method == 'POST':
        msg = 'Porfavor rellene la forma'
    return render_template('register.html', msg=msg)

if __name__ == "__main__":
    app.run(port=5000, debug=True)