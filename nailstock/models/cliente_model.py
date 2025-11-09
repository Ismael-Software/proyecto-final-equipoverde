from database.db_connection import get_db_connection

class ClienteModel:
    @staticmethod
    def agregar_cliente(nombre, telefono, direccion, rfc):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (nombre, telefono, direccion, rfc)
            VALUES (?, ?, ?, ?)
        ''', (nombre, telefono, direccion, rfc))
        
        cliente_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return cliente_id
    
    @staticmethod
    def obtener_clientes():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes ORDER BY nombre')
        clientes = cursor.fetchall()
        conn.close()
        
        return clientes
    
    @staticmethod
    def obtener_cliente_por_id(cliente_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        cliente = cursor.fetchone()
        conn.close()
        
        return cliente
    
    @staticmethod
    def actualizar_cliente(cliente_id, nombre, telefono, direccion, rfc):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE clientes 
            SET nombre = ?, telefono = ?, direccion = ?, rfc = ?
            WHERE id = ?
        ''', (nombre, telefono, direccion, rfc, cliente_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    @staticmethod
    def eliminar_cliente(cliente_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si hay ventas asociadas
        cursor.execute('SELECT COUNT(*) FROM ventas WHERE cliente_id = ?', (cliente_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            raise Exception("No se puede eliminar el cliente porque tiene ventas asociadas")
        
        cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()
        conn.close()
        
        return True