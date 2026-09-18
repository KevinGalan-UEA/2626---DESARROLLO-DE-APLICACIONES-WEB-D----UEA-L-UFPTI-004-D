from types import SimpleNamespace

import mysql.connector
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion
from models import Usuario
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-hibrido-ganador-2026'  # cámbiala antes de producción
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)


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
# Autenticación
# ---------------------------------------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = UsuarioForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
                (form.usuario.data, password_hash)
            )
            conn.commit()
            flash(f'Usuario "{form.usuario.data}" registrado correctamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            conn.rollback()
            flash('Ese nombre de usuario ya existe. Elige otro.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        fila = Usuario.obtener_por_usuario(form.usuario.data)
        if fila and check_password_hash(fila['password'], form.password.data):
            usuario_obj = Usuario(id=fila['id'], usuario=fila['usuario'])
            login_user(usuario_obj)
            flash(f'Bienvenido, {usuario_obj.usuario}.', 'success')
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ---------------------------------------------------------
# Clientes (protegido)
# ---------------------------------------------------------
@app.route('/clientes')
@login_required
def clientes():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes ORDER BY id_cliente')
    clientes_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_bd, total_clientes=len(clientes_bd))


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
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
# Productos (protegido) — CRUD completo con MySQL
# ---------------------------------------------------------
@app.route('/productos')
@login_required
def productos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos ORDER BY id_producto')
    productos_bd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos_bd, delete_form=AccionForm())


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
# Facturación (protegido) — con JOIN a Clientes
# ---------------------------------------------------------
@app.route('/facturacion')
@login_required
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
@login_required
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