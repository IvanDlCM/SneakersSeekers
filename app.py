from flask import Flask, render_template, request, url_for, redirect
import mysql.connector

app = Flask(__name__)

midb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ss"
)

cursor = midb.cursor(dictionary=True)

@app.route('/')
def inicio():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos limit 3')
    muestras = cursor.fetchall()
    return render_template('index.html', muestras=muestras)

@app.route('/marcas')
def marcas():
    return render_template('marcas.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

def obtener_producto(id):
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    return producto

def obtener_relacionados(id):
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id != %s", (id,))
    productos_relacionados = cursor.fetchall()
    return productos_relacionados

@app.route('/productos/')
def productos():
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/productos/<int:id>')
def producto(id):
    producto = obtener_producto(id)
    productos_relacionados = obtener_relacionados(id)
    return render_template('producto.html', producto=producto, productos_relacionados=productos_relacionados)

@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.form['imagen']
        if (nombre !='') and (descripcion != '') and (precio != '') and (imagen != ''):
            if not midb.is_connected():
                midb.connect()
            cursor = midb.cursor(dictionary=True)
            cursor.execute("INSERT INTO productos (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)", (nombre, descripcion, precio, imagen))
            midb.commit()
            cursor.close()
            midb.close()
            return redirect(url_for('productos'))
        else:
            return redirect(url_for('productos'))

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    midb.commit()
    cursor.close()
    return redirect(url_for('productos'))

@app.route('/productos/<int:id>/actualizar', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    imagen = request.form['imagen']
    if (nombre !='') and (descripcion != '') and (precio != '') and (imagen != ''):
        if not midb.is_connected():
            midb.connect()
        cursor = midb.cursor(dictionary=True)
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, imagen = %s WHERE id = %s", (nombre, descripcion, precio, imagen, id))
        midb.commit()
        cursor.close()
        midb.close()
        return redirect(url_for('productos'))
    else:
        return redirect(url_for('productos'))