from database.db_connection import get_db_connection

class ProductoModel:
    @staticmethod
    def agregar_producto(nombre, descripcion, categoria, precio_compra, precio_venta, 
                        stock, stock_minimo, unidad, proveedor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, categoria, precio_compra, 
                                     precio_venta, stock, stock_minimo, unidad, proveedor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, descripcion, categoria, precio_compra, precio_venta, 
                  stock, stock_minimo, unidad, proveedor_id))
            
            producto_id = cursor.lastrowid
            conn.commit()
            return producto_id
        finally:
            conn.close()
    
    @staticmethod
    def obtener_productos(activo=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.*, pr.nombre as proveedor_nombre 
                FROM productos p 
                LEFT JOIN proveedores pr ON p.proveedor_id = pr.id 
                WHERE p.activo = ?
                ORDER BY p.nombre
            ''', (activo,))
            
            productos = cursor.fetchall()
            return productos
        finally:
            conn.close()
    
    @staticmethod
    def obtener_producto_por_id(producto_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.*, pr.nombre as proveedor_nombre 
                FROM productos p 
                LEFT JOIN proveedores pr ON p.proveedor_id = pr.id 
                WHERE p.id = ?
            ''', (producto_id,))
            
            producto = cursor.fetchone()
            return producto
        finally:
            conn.close()
    
    @staticmethod
    def actualizar_producto(producto_id, nombre, descripcion, categoria, precio_compra, 
                           precio_venta, stock, stock_minimo, unidad, proveedor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE productos 
                SET nombre = ?, descripcion = ?, categoria = ?, precio_compra = ?,
                    precio_venta = ?, stock = ?, stock_minimo = ?, unidad = ?, proveedor_id = ?
                WHERE id = ?
            ''', (nombre, descripcion, categoria, precio_compra, precio_venta,
                  stock, stock_minimo, unidad, proveedor_id, producto_id))
            
            conn.commit()
            return True
        finally:
            conn.close()
    
    @staticmethod
    def eliminar_producto(producto_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Inactivo, no se elimna realmente .
            cursor.execute('UPDATE productos SET activo = 0 WHERE id = ?', (producto_id,))
            conn.commit()
            return True
        finally:
            conn.close()
    
    @staticmethod
    def buscar_productos(termino):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.*, pr.nombre as proveedor_nombre 
                FROM productos p 
                LEFT JOIN proveedores pr ON p.proveedor_id = pr.id 
                WHERE p.activo = 1 AND (p.nombre LIKE ? OR p.descripcion LIKE ?)
                ORDER BY p.nombre
            ''', (f'%{termino}%', f'%{termino}%'))
            
            productos = cursor.fetchall()
            return productos
        finally:
            conn.close()