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
    return render_template('index.html')

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
    cursor.execute(f"SELECT * FROM productos WHERE id = {id}")
    producto = cursor.fetchone()
    return producto

def obtener_relacionados(id):
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM productos WHERE id != {id}")
    productos_relacionados = cursor.fetchall()
    return productos_relacionados

@app.route('/productos/')
def productos():
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute('select * from productos')
    productos = cursor.fetchall()
    return render_template('todosProductos.html', productos=productos)

@app.route('/productos/<int:id>')
def producto(id):
    producto = obtener_producto(id)
    productos_relacionados = obtener_relacionados(id)
    return render_template('producto.html', producto=producto, productos_relacionados=productos_relacionados)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    cursor.execute(f"delete from productos WHERE id = {id}")
    midb.commit()
    cursor.close()

    return redirect(url_for('productos'))

@app.route('/productos/<int:id>/editar', methods=['GET'])
def editar_producto(id):
    producto = obtener_producto(id)
    # Mostrar el formulario de actualización con los detalles del producto
    return render_template('editar_producto.html', producto=producto)

@app.route('/productos/<int:id>/guardar', methods=['POST'])
def guardar_cambios(id):
    if not midb.is_connected():
        midb.connect()
    cursor = midb.cursor(dictionary=True)
    # Obtener los datos actualizados del formulario
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    imagen = request.form['imagen']
    # Actualizar el producto en la base de datos
    cursor.execute(f"UPDATE productos SET nombre = '{nombre}', descripcion = '{descripcion}', precio = '{precio}',"
                   f" imagen = '{imagen}' WHERE id = {id}")
    midb.commit()
    cursor.close()
    midb.close()
    # Redirigir al usuario de regreso a la vista de detalles del producto actualizado
    return redirect(url_for('producto', id=id))



@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.form['imagen']

        if not midb.is_connected():
            midb.connect()
        cursor = midb.cursor(dictionary=True)
        cursor.execute(f"INSERT INTO productos (nombre, descripcion, precio, imagen) VALUES ('{nombre}', '{descripcion}"
                       f"', '{precio}', '{imagen}')")
        midb.commit()
        cursor.close()
        midb.close()
        # Redirigir al usuario a la página de productos
        return redirect(url_for('productos'))

    # Renderizar el formulario para ingresar nuevos productos
    return render_template('nuevo_producto.html')

