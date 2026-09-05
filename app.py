import os
import sqlite3

from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-hibrido-ganador-2026'  # cámbiala antes de producción

# Diccionario con información general de la empresa
empresa = {
    "nombre": "El Híbrido Ganador",
    "eslogan": "Plataforma para la gestión de clientes, cotizaciones y soporte técnico en instalación de redes, seguridad y automatización residencial.",
    "anio_fundacion": 2026
}

# ---------------------------------------------------------
# Configuración de la base de datos SQLite
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'hibrido_ganador.db')

os.makedirs(DATA_DIR, exist_ok=True)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a las columnas por nombre (producto.nombre, producto.precio, etc.)
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            imagen TEXT
        )
    ''')

    # Si la tabla está vacía, la llenamos con los productos de demostración
    # que ya tenías, para no perder ese contenido.
    total = conn.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    if total == 0:
        productos_iniciales = [
            ("Router Wi-Fi 6", "Conectividad", 85.00, 12, "router.jpg"),
            ("Cámara PoE 4MP", "Videovigilancia", 45.50, 5, "camara.jpg"),
            ("Kit Domótica Básico", "Domótica", 120.00, 0, "domotica.jpg"),
            ("Switch 8 puertos", "Conectividad", 35.00, 8, "switch.jpg"),
            ("Sensor de Movimiento", "Domótica", 18.75, 20, "sensor.jpg"),
            ("Cámara Wi-Fi Exterior", "Videovigilancia", 62.00, 0, "camara-exterior.jpg"),
            ("Repetidor de Señal", "Conectividad", 27.90, 15, "repetidor.jpg"),
        ]
        conn.executemany(
            'INSERT INTO productos (nombre, categoria, precio, stock, imagen) VALUES (?, ?, ?, ?, ?)',
            productos_iniciales
        )
        conn.commit()

    conn.close()


init_db()

# ---------------------------------------------------------
# Clientes y Facturación siguen en memoria (sin cambios esta semana)
# ---------------------------------------------------------
clientes_data = [
    {"id": 1, "nombre": "Juan Pérez", "correo": "juan@mail.com", "telefono": "0991234567", "direccion": "Av. Amazonas y Naciones Unidas, Puyo", "activo": True},
    {"id": 2, "nombre": "María Gómez", "correo": "maria@mail.com", "telefono": "0987654321", "direccion": "Barrio Central, Puyo", "activo": True},
    {"id": 3, "nombre": "Carlos Ruiz", "correo": "carlos@mail.com", "telefono": "0965432189", "direccion": "Vía a Shell km 3", "activo": False},
    {"id": 4, "nombre": "Ana Torres", "correo": "ana.torres@mail.com", "telefono": "0978123456", "direccion": "Ciudadela Los Ceibos, Puyo", "activo": True},
    {"id": 5, "nombre": "Luis Mendoza", "correo": "luis.mendoza@mail.com", "telefono": "0956781234", "direccion": "Barrio 24 de Mayo", "activo": False},
]

facturas_data = [
    {"numero": "F-0001", "cliente": "Juan Pérez", "total": 165.50, "estado": "Pendiente"},
]


@app.route('/')
def index():
    return render_template('index.html', empresa=empresa)


# ---------------------------------------------------------
# Clientes (sin cambios)
# ---------------------------------------------------------
@app.route('/clientes')
def clientes():
    total_clientes = len(clientes_data)
    return render_template('clientes.html', clientes=clientes_data, total_clientes=total_clientes)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_id = (max(c['id'] for c in clientes_data) + 1) if clientes_data else 1
        clientes_data.append({
            "id": nuevo_id,
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "direccion": form.direccion.data,
            "activo": form.activo.data
        })
        flash(f'Cliente "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)


# ---------------------------------------------------------
# Productos — ahora con SQLite
# ---------------------------------------------------------
@app.route('/productos')
def productos():
    conn = get_db_connection()
    productos_bd = conn.execute('SELECT * FROM productos ORDER BY id').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos_bd)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO productos (nombre, categoria, precio, stock, imagen) VALUES (?, ?, ?, ?, ?)',
            (form.nombre.data, form.categoria.data, float(form.precio.data), form.stock.data, 'default.jpg')
        )
        conn.commit()
        conn.close()
        flash(f'Producto "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)


# ---------------------------------------------------------
# Facturación (sin cambios)
# ---------------------------------------------------------
@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=facturas_data)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_factura():
    form = FacturacionForm()
    if form.validate_on_submit():
        numero = f"F-{len(facturas_data) + 1:04d}"
        facturas_data.append({
            "numero": numero,
            "cliente": form.cliente.data,
            "total": float(form.total.data),
            "estado": form.estado.data
        })
        flash(f'Factura {numero} registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)