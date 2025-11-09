from database.db_connection import get_db_connection
import csv

class Reportes:
    @staticmethod
    def exportar_productos_csv(ruta_archivo):
        """Exporta todos los productos a un archivo CSV"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.nombre, p.descripcion, p.categoria, p.precio_compra, 
                   p.precio_venta, p.stock, p.stock_minimo, p.unidad, 
                   pr.nombre as proveedor, p.fecha_creacion
            FROM productos p 
            LEFT JOIN proveedores pr ON p.proveedor_id = pr.id 
            WHERE p.activo = 1
            ORDER BY p.nombre
        ''')
        
        productos = cursor.fetchall()
        conn.close()
        
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                'ID', 'Nombre', 'Descripción', 'Categoría', 'Precio Compra', 
                'Precio Venta', 'Stock', 'Stock Mínimo', 'Unidad', 'Proveedor', 'Fecha Creación'
            ])
            
            for producto in productos:
                writer.writerow(producto)
        
        return ruta_archivo
    
    @staticmethod
    def exportar_ventas_csv(ruta_archivo, fecha_inicio=None, fecha_fin=None):
        """Exporta ventas a un archivo CSV"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT v.id, c.nombre as cliente, u.nombre as vendedor, 
                   v.total, v.fecha_venta
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
        
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                'ID Venta', 'Cliente', 'Vendedor', 'Total', 'Fecha Venta'
            ])
            
            for venta in ventas:
                writer.writerow(venta)
        
        return ruta_archivo
    
    @staticmethod
    def exportar_clientes_csv(ruta_archivo):
        """Exporta todos los clientes a un archivo CSV"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes ORDER BY nombre')
        clientes = cursor.fetchall()
        conn.close()
        
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID', 'Nombre', 'Teléfono', 'Dirección', 'RFC', 'Fecha Creación'])
            
            for cliente in clientes:
                writer.writerow(cliente)
        
        return ruta_archivo
    
    @staticmethod
    def generar_reporte_ventas_por_periodo(fecha_inicio, fecha_fin):
        """Genera un reporte de ventas por periodo con estadísticas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_ventas,
                SUM(total) as ingresos_totales,
                AVG(total) as promedio_venta,
                MIN(total) as venta_minima,
                MAX(total) as venta_maxima
            FROM ventas 
            WHERE DATE(fecha_venta) BETWEEN ? AND ?
        ''', (fecha_inicio, fecha_fin))
        
        estadisticas = cursor.fetchone()
        
        # Ventas por día
        cursor.execute('''
            SELECT DATE(fecha_venta), COUNT(*), SUM(total)
            FROM ventas 
            WHERE DATE(fecha_venta) BETWEEN ? AND ?
            GROUP BY DATE(fecha_venta)
            ORDER BY DATE(fecha_venta)
        ''', (fecha_inicio, fecha_fin))
        
        ventas_por_dia = cursor.fetchall()
        
        # Productos más vendidos
        cursor.execute('''
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.subtotal) as ingresos
            FROM detalle_venta dv
            JOIN productos p ON dv.producto_id = p.id
            JOIN ventas v ON dv.venta_id = v.id
            WHERE DATE(v.fecha_venta) BETWEEN ? AND ?
            GROUP BY p.id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT 10
        ''', (fecha_inicio, fecha_fin))
        
        productos_populares = cursor.fetchall()
        
        conn.close()
        
        return {
            'estadisticas': {
                'total_ventas': estadisticas[0] or 0,
                'ingresos_totales': estadisticas[1] or 0,
                'promedio_venta': estadisticas[2] or 0,
                'venta_minima': estadisticas[3] or 0,
                'venta_maxima': estadisticas[4] or 0
            },
            'ventas_por_dia': ventas_por_dia,
            'productos_populares': productos_populares
        }
    
    @staticmethod
    def generar_reporte_stock():
        """Genera reporte de situación de stock"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Productos con stock bajo
        cursor.execute('''
            SELECT nombre, stock, stock_minimo, unidad
            FROM productos 
            WHERE activo = 1 AND stock <= stock_minimo
            ORDER BY stock ASC
        ''')
        
        stock_bajo = cursor.fetchall()
        
        # Productos sin stock
        cursor.execute('''
            SELECT nombre, stock, stock_minimo, unidad
            FROM productos 
            WHERE activo = 1 AND stock = 0
            ORDER BY nombre
        ''')
        
        sin_stock = cursor.fetchall()
        
        # Valor total del inventario
        cursor.execute('''
            SELECT SUM(stock * precio_compra) as valor_inventario
            FROM productos 
            WHERE activo = 1
        ''')
        
        valor_inventario = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'stock_bajo': stock_bajo,
            'sin_stock': sin_stock,
            'valor_inventario': valor_inventario
        }