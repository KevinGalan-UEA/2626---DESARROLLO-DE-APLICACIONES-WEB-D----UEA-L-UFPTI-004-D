-- Esquema de base de datos - El Híbrido Ganador

CREATE DATABASE IF NOT EXISTS hibrido_ganador_db;
USE hibrido_ganador_db;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    imagen VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Datos de demostración (solo se insertan la primera vez que se ejecuta todo el script)
INSERT INTO clientes (nombre, correo, telefono, direccion, activo) VALUES
('Juan Pérez', 'juan@mail.com', '0991234567', 'Av. Amazonas y Naciones Unidas, Puyo', TRUE),
('María Gómez', 'maria@mail.com', '0987654321', 'Barrio Central, Puyo', TRUE),
('Carlos Ruiz', 'carlos@mail.com', '0965432189', 'Vía a Shell km 3', FALSE),
('Ana Torres', 'ana.torres@mail.com', '0978123456', 'Ciudadela Los Ceibos, Puyo', TRUE),
('Luis Mendoza', 'luis.mendoza@mail.com', '0956781234', 'Barrio 24 de Mayo', FALSE);

INSERT INTO productos (nombre, categoria, precio, stock, imagen) VALUES
('Router Wi-Fi 6', 'Conectividad', 85.00, 12, 'router.jpg'),
('Cámara PoE 4MP', 'Videovigilancia', 45.50, 5, 'camara.jpg'),
('Kit Domótica Básico', 'Domótica', 120.00, 0, 'domotica.jpg'),
('Switch 8 puertos', 'Conectividad', 35.00, 8, 'switch.jpg'),
('Sensor de Movimiento', 'Domótica', 18.75, 20, 'sensor.jpg'),
('Cámara Wi-Fi Exterior', 'Videovigilancia', 62.00, 0, 'camara-exterior.jpg'),
('Repetidor de Señal', 'Conectividad', 27.90, 15, 'repetidor.jpg');

INSERT INTO facturas (id_cliente, total, estado) VALUES
(1, 165.50, 'Pendiente');