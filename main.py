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

app.secret_key = "mysecretkey"


@app.route('/inventoryflask/', methods=['GET', 'POST'])
def login():
    msg = ' '
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
            return redirect(url_for('home'))
        else:
            msg = 'Datos incorrectos'
    return render_template('index.html', msg=msg)

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

@app.route('/inventoryflask/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/inventoryflask/categories')
def categories():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'nombre' in request.form:
            nombre = request.form['nombre']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM marcas)
            cursor.execute('INSERT INTO marcas VALUES (NULL, %s, " ", " ")', [nombre])
            mysql.connection.commit()
            msg = 'Esta registrado en la base de datos'
        return render_template('company.html', username=session['username'], msg=msg)
    return redirect(url_for('login'))

@app.route('/inventoryflask/company', methods=['GET', 'POST'])
def company():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'nombre' in request.form:
            nombre = request.form['nombre']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO marcas VALUES (NULL, %s, " ", " ")', [nombre])
            mysql.connection.commit()
            msg = 'Esta registrado en la base de datos'
        return render_template('company.html', username=session['username'], msg=msg)
    return redirect(url_for('login'))

@app.route('/inventoryflask/products')
def products():
    if 'loggedin' in session:
        return render_template('products.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/inventoryflask/providers')
def providers():
    if 'loggedin' in session:
        return render_template('providers.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/inventoryflask/saletype')
def saletype():
    if 'loggedin' in session:
        return render_template('sale-type.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/inventoryflask/state')
def state():
    if 'loggedin' in session:
        return render_template('state.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/inventoryflask/subcategories')
def subcategories():
    if 'loggedin' in session:
        return render_template('subcategories.html', username=session['username'])
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)