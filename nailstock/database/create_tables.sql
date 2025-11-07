-- Tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT,
    correo TEXT,
    rfc TEXT,
    observaciones TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT,
    rfc TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    precio_compra REAL NOT NULL,
    precio_venta REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    unidad TEXT NOT NULL,
    proveedor_id INTEGER,
    activo BOOLEAN DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
);

-- Tabla de ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    total REAL NOT NULL,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

-- Tabla de detalle_venta
CREATE TABLE IF NOT EXISTS detalle_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas (id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);

-- Triggers

-- Disminuir stock al registrar venta
CREATE TRIGGER IF NOT EXISTS disminuir_stock_venta
AFTER INSERT ON detalle_venta
FOR EACH ROW
BEGIN
    UPDATE productos 
    SET stock = stock - NEW.cantidad 
    WHERE id = NEW.producto_id;
END;

-- Aumentar stock al eliminar venta
CREATE TRIGGER IF NOT EXISTS aumentar_stock_eliminar_venta
AFTER DELETE ON detalle_venta
FOR EACH ROW
BEGIN
    UPDATE productos 
    SET stock = stock + OLD.cantidad 
    WHERE id = OLD.producto_id;
END;

-- Trigger para prevenir stock negativo
CREATE TRIGGER IF NOT EXISTS prevenir_stock_negativo
BEFORE UPDATE ON productos
FOR EACH ROW
WHEN NEW.stock < 0
BEGIN
    SELECT RAISE(ABORT, 'No se puede tener stock negativo');
END;
