from flask import Flask, render_template

app = Flask(__name__)

# Diccionario con información general de la empresa
empresa = {
    "nombre": "El Híbrido Ganador",
    "eslogan": "Plataforma para la gestión de clientes, cotizaciones y soporte técnico en instalación de redes, seguridad y automatización residencial.",
    "anio_fundacion": 2026
}


@app.route('/')
def index():
    return render_template('index.html', empresa=empresa)


@app.route('/clientes')
def clientes():
    lista_clientes = [
        {"id": 1, "nombre": "Juan Pérez", "correo": "juan@mail.com", "telefono": "0991234567", "direccion": "Av. Amazonas y Naciones Unidas, Puyo", "activo": True},
        {"id": 2, "nombre": "María Gómez", "correo": "maria@mail.com", "telefono": "0987654321", "direccion": "Barrio Central, Puyo", "activo": True},
        {"id": 3, "nombre": "Carlos Ruiz", "correo": "carlos@mail.com", "telefono": "0965432189", "direccion": "Vía a Shell km 3", "activo": False},
        {"id": 4, "nombre": "Ana Torres", "correo": "ana.torres@mail.com", "telefono": "0978123456", "direccion": "Ciudadela Los Ceibos, Puyo", "activo": True},
        {"id": 5, "nombre": "Luis Mendoza", "correo": "luis.mendoza@mail.com", "telefono": "0956781234", "direccion": "Barrio 24 de Mayo", "activo": False},
    ]
    total_clientes = len(lista_clientes)
    return render_template('clientes.html', clientes=lista_clientes, total_clientes=total_clientes)


@app.route('/productos')
def productos():
    lista_productos = [
        {"nombre": "Router Wi-Fi 6", "categoria": "Conectividad", "precio": 85.00, "stock": 12, "imagen": "router.jpg"},
        {"nombre": "Cámara PoE 4MP", "categoria": "Videovigilancia", "precio": 45.50, "stock": 5, "imagen": "camara.jpg"},
        {"nombre": "Kit Domótica Básico", "categoria": "Domótica", "precio": 120.00, "stock": 0, "imagen": "domotica.jpg"},
        {"nombre": "Switch 8 puertos", "categoria": "Conectividad", "precio": 35.00, "stock": 8, "imagen": "switch.jpg"},
        {"nombre": "Sensor de Movimiento", "categoria": "Domótica", "precio": 18.75, "stock": 20, "imagen": "sensor.jpg"},
        {"nombre": "Cámara Wi-Fi Exterior", "categoria": "Videovigilancia", "precio": 62.00, "stock": 0, "imagen": "camara-exterior.jpg"},
        {"nombre": "Repetidor de Señal", "categoria": "Conectividad", "precio": 27.90, "stock": 15, "imagen": "repetidor.jpg"},
    ]
    return render_template('productos.html', productos=lista_productos)


@app.route('/facturacion')
def facturacion():
    factura_actual = {
        "numero": "F-0001",
        "cliente": "Juan Pérez",
        "total": 165.50,
        "estado": "Pendiente"
    }
    return render_template('facturacion.html', factura=factura_actual)


if __name__ == '__main__':
    app.run(debug=True)