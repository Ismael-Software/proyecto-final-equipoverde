from database.db_connection import get_db_connection

class VentaModel:
    @staticmethod
    def agregar_venta(cliente_id, usuario_id, productos):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Calcular total
            total = sum(item['cantidad'] * item['precio_unitario'] for item in productos)
            
            # Insertar venta
            cursor.execute('''
                INSERT INTO ventas (cliente_id, usuario_id, total)
                VALUES (?, ?, ?)
            ''', (cliente_id, usuario_id, total))
            
            venta_id = cursor.lastrowid
            
            # Insertar detallesde venta
            for producto in productos:
                subtotal = producto['cantidad'] * producto['precio_unitario']
                cursor.execute('''
                    INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venta_id, producto['producto_id'], producto['cantidad'], 
                      producto['precio_unitario'], subtotal))
            
            conn.commit()
            return venta_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_ventas(fecha_inicio=None, fecha_fin=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT v.*, c.nombre as cliente_nombre, u.nombre as usuario_nombre
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN usuarios u ON v.usuario_id = u.id
        '''
        
        params = []
        
        if fecha_inicio and fecha_fin:
            query += ' WHERE DATE(v.fecha_venta) BETWEEN ? AND ?'
            params.extend([fecha_inicio, fecha_fin])
        
        query += ' ORDER BY v.fecha_venta DESC'
        
        cursor.execute(query, params)
        ventas = cursor.fetchall()
        conn.close()
        
        return ventas
    
    @staticmethod
    def obtener_detalle_venta(venta_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dv.*, p.nombre as producto_nombre, p.unidad
            FROM detalle_venta dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        ''', (venta_id,))
        
        detalle = cursor.fetchall()
        conn.close()
        
        return detalle
    
    @staticmethod
    def eliminar_venta(venta_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Eliminar venta (los triggers se encargarán de restaurar el stock)
            cursor.execute('DELETE FROM ventas WHERE id = ?', (venta_id,))
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()