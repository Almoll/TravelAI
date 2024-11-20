CREATE DATABASE SistemaViajes;

USE SistemaViajes;

-- Tabla para los usuarios
CREATE TABLE Usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    perfil_completado BOOLEAN DEFAULT FALSE
);

-- Tabla para los perfiles de usuarios
CREATE TABLE Perfiles (
    perfil_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    idioma VARCHAR(50) DEFAULT 'es',
    moneda VARCHAR(10) DEFAULT 'USD',
    notificaciones BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla para destinos
CREATE TABLE Destinos (
    destino_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    costo_estimado DECIMAL(10,2),
    categoria VARCHAR(50)
);

-- Tabla central para viajes
CREATE TABLE Viajes (
    viaje_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    destino_id INT NOT NULL,
    nombre VARCHAR(255),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    presupuesto DECIMAL(10,2),
    estado VARCHAR(50) DEFAULT 'Pendiente', -- Ej.: Pendiente, En Curso, Completado
    tipo_transporte VARCHAR(50),
    comentarios TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (destino_id) REFERENCES Destinos(destino_id)
);

-- Tabla para actividades relacionadas con viajes
CREATE TABLE Actividades (
    actividad_id INT AUTO_INCREMENT PRIMARY KEY,
    viaje_id INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    duracion_estimada DECIMAL(4,2),
    costo DECIMAL(10,2),
    horario_disponible VARCHAR(255),
    fecha DATE,
    hora TIME,
    FOREIGN KEY (viaje_id) REFERENCES Viajes(viaje_id)
);

-- Tabla para notificaciones
CREATE TABLE Notificaciones (
    notificacion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- Tabla para recomendaciones personalizadas
CREATE TABLE Recomendaciones (
    recomendacion_id INT AUTO_INCREMENT PRIMARY KEY,
    viaje_id INT NOT NULL,
    actividad_id INT,
    motivo VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (viaje_id) REFERENCES Viajes(viaje_id),
    FOREIGN KEY (actividad_id) REFERENCES Actividades(actividad_id)
);
