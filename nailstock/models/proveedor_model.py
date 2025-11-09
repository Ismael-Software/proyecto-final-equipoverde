from database.db_connection import get_db_connection

class ProveedorModel:
    @staticmethod
    def agregar_proveedor(nombre, telefono, direccion, correo, rfc, observaciones):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO proveedores (nombre, telefono, direccion, correo, rfc, observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, telefono, direccion, correo, rfc, observaciones))
        
        proveedor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return proveedor_id
    
    @staticmethod
    def obtener_proveedores():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM proveedores ORDER BY nombre')
        proveedores = cursor.fetchall()
        conn.close()
        
        return proveedores
    
    @staticmethod
    def obtener_proveedor_por_id(proveedor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM proveedores WHERE id = ?', (proveedor_id,))
        proveedor = cursor.fetchone()
        conn.close()
        
        return proveedor
    
    @staticmethod
    def actualizar_proveedor(proveedor_id, nombre, telefono, direccion, correo, rfc, observaciones):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE proveedores 
            SET nombre = ?, telefono = ?, direccion = ?, correo = ?, rfc = ?, observaciones = ?
            WHERE id = ?
        ''', (nombre, telefono, direccion, correo, rfc, observaciones, proveedor_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    @staticmethod
    def eliminar_proveedor(proveedor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si hay productos asociados
        cursor.execute('SELECT COUNT(*) FROM productos WHERE proveedor_id = ?', (proveedor_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            raise Exception("No se puede eliminar el proveedor porque tiene productos asociados")
        
        cursor.execute('DELETE FROM proveedores WHERE id = ?', (proveedor_id,))
        conn.commit()
        conn.close()
        
        return True