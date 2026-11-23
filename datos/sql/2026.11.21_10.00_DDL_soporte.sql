-- Creación de tablas del sistema de tickets (Evaluación 2)
-- Para ejecutarlo a mano: CREATE DATABASE soporte_tickets; USE soporte_tickets;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tecnicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    especialidad VARCHAR(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(300) NOT NULL,
    fecha_creacion DATETIME NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Abierto',
    prioridad VARCHAR(20) NOT NULL DEFAULT 'Media',
    usuario_id INT NOT NULL,
    tecnico_id INT NULL,
    CONSTRAINT fk_ticket_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    CONSTRAINT fk_ticket_tecnico FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS acciones_soporte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(300) NOT NULL,
    fecha DATETIME NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    ticket_id INT NOT NULL,
    tecnico_id INT NOT NULL,
    CONSTRAINT fk_accion_ticket FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
    CONSTRAINT fk_accion_tecnico FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
