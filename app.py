from types import SimpleNamespace

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from conexion.conexion import obtener_conexion
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-hibrido-ganador-2026'  # cámbiala antes de producción
csrf = CSRFProtect(app)


class AccionForm(FlaskForm):
    """Formulario vacío, solo para generar el token CSRF en el botón de Eliminar."""
    pass


empresa = {
    "nombre": "El Híbrido Ganador",
    "eslogan": "Plataforma para la gestión de clientes, cotizaciones y soporte técnico en instalación de redes, seguridad y automatización residencial.",
    "anio_fundacion": 2026
}


@app.route('/')
def index():
    return render_template('index.html', empresa=empresa)


# ---------------------------------------------------------
# Clientes — listar y agregar, ahora desde MySQL
# ---------------------------------------------------------
@app.route('/clientes')
def clientes():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes ORDER BY id_cliente')
    clientes_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_bd, total_clientes=len(clientes_bd))


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO clientes (nombre, correo, telefono, direccion, activo) VALUES (%s, %s, %s, %s, %s)',
            (form.nombre.data, form.correo.data, form.telefono.data, form.direccion.data, form.activo.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash(f'Cliente "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)


# ---------------------------------------------------------
# Productos — CRUD completo con MySQL (SELECT, INSERT, UPDATE, DELETE)
# ---------------------------------------------------------
@app.route('/productos')
def productos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos ORDER BY id_producto')
    productos_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos_bd, delete_form=AccionForm())


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, categoria, precio, stock, imagen) VALUES (%s, %s, %s, %s, %s)',
            (form.nombre.data, form.categoria.data, float(form.precio.data), form.stock.data, 'default.jpg')
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash(f'Producto "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form, modo='nuevo')


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto_bd = cursor.fetchone()
    cursor.close()

    if producto_bd is None:
        conn.close()
        flash('El producto que intentas editar no existe.', 'danger')
        return redirect(url_for('productos'))

    if request.method == 'GET':
        form = ProductoForm(obj=SimpleNamespace(**producto_bd))
    else:
        form = ProductoForm()

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE productos SET nombre = %s, categoria = %s, precio = %s, stock = %s WHERE id_producto = %s',
            (form.nombre.data, form.categoria.data, float(form.precio.data), form.stock.data, id_producto)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash(f'Producto "{form.nombre.data}" actualizado correctamente.', 'success')
        return redirect(url_for('productos'))

    conn.close()
    return render_template('formulario_producto.html', form=form, modo='editar', id_producto=id_producto)


@app.route('/productos/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos'))


# ---------------------------------------------------------
# Facturación — listar (con JOIN a Clientes) y agregar, desde MySQL
# ---------------------------------------------------------
@app.route('/facturacion')
def facturacion():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT f.id_factura, f.total, f.estado, f.fecha, c.nombre AS cliente_nombre
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura
    ''')
    facturas_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', facturas=facturas_bd)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_factura():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id_cliente, nombre FROM clientes ORDER BY nombre')
    clientes_bd = cursor.fetchall()
    cursor.close()

    form = FacturacionForm()
    form.id_cliente.choices = [(c['id_cliente'], c['nombre']) for c in clientes_bd]

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO facturas (id_cliente, total, estado) VALUES (%s, %s, %s)',
            (form.id_cliente.data, float(form.total.data), form.estado.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))

    conn.close()
    return render_template('formulario_facturacion.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)