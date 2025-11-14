from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QDateEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QFileDialog, QGroupBox, QFormLayout)
from PyQt6.QtCore import QDate, Qt
from datetime import datetime, timedelta
from utils.reportes import Reportes
from utils.mensajes import Mensajes

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Grupo de exportación
        export_group = QGroupBox("Exportar Datos")
        export_layout = QVBoxLayout()
        
        # Botones de exportación
        btn_export_productos = QPushButton("Exportar Productos a CSV")
        btn_export_ventas = QPushButton("Exportar Ventas a CSV")
        btn_export_clientes = QPushButton("Exportar Clientes a CSV")
        
        btn_export_productos.clicked.connect(self.exportar_productos)
        btn_export_ventas.clicked.connect(self.exportar_ventas)
        btn_export_clientes.clicked.connect(self.exportar_clientes)
        
        export_layout.addWidget(btn_export_productos)
        export_layout.addWidget(btn_export_ventas)
        export_layout.addWidget(btn_export_clientes)
        export_group.setLayout(export_layout)
        
        # Grupo de reportes
        reportes_group = QGroupBox("Reportes Especializados")
        reportes_layout = QFormLayout()
        
        # Fechas para reporte de ventas
        fecha_layout = QHBoxLayout()
        
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setDate(QDate.currentDate().addDays(-30))
        self.fecha_inicio.setCalendarPopup(True)
        
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setCalendarPopup(True)
        
        fecha_layout.addWidget(QLabel("Desde:"))
        fecha_layout.addWidget(self.fecha_inicio)
        fecha_layout.addWidget(QLabel("Hasta:"))
        fecha_layout.addWidget(self.fecha_fin)
        
        btn_reporte_ventas = QPushButton("Generar Reporte de Ventas")
        btn_reporte_stock = QPushButton("Generar Reporte de Stock")
        
        btn_reporte_ventas.clicked.connect(self.generar_reporte_ventas)
        btn_reporte_stock.clicked.connect(self.generar_reporte_stock)
        
        reportes_layout.addRow("Período:", fecha_layout)
        reportes_layout.addRow(btn_reporte_ventas)
        reportes_layout.addRow(btn_reporte_stock)
        reportes_group.setLayout(reportes_layout)
        
        # Tabla para mostrar resultados
        self.table_resultados = QTableWidget()
        self.table_resultados.setColumnCount(0)
        
        layout.addWidget(export_group)
        layout.addWidget(reportes_group)
        layout.addWidget(QLabel("Resultados:"))
        layout.addWidget(self.table_resultados)
        
        self.setLayout(layout)
    
    def exportar_productos(self):
        try:
            ruta_archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar Productos como CSV", 
                f"productos_{datetime.now().strftime('%Y%m%d')}.csv",
                "Archivos CSV (*.csv)"
            )
            
            if ruta_archivo:
                Reportes.exportar_productos_csv(ruta_archivo)
                Mensajes.mostrar_exito(f"Productos exportados correctamente a:\n{ruta_archivo}", self)
        
        except Exception as e:
            Mensajes.mostrar_error(f"Error al exportar productos: {str(e)}", self)
    
    def exportar_ventas(self):
        try:
            ruta_archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar Ventas como CSV", 
                f"ventas_{datetime.now().strftime('%Y%m%d')}.csv",
                "Archivos CSV (*.csv)"
            )
            
            if ruta_archivo:
                fecha_inicio = self.fecha_inicio.date().toString('yyyy-MM-dd')
                fecha_fin = self.fecha_fin.date().toString('yyyy-MM-dd')
                
                Reportes.exportar_ventas_csv(ruta_archivo, fecha_inicio, fecha_fin)
                Mensajes.mostrar_exito(f"Ventas exportadas correctamente a:\n{ruta_archivo}", self)
        
        except Exception as e:
            Mensajes.mostrar_error(f"Error al exportar ventas: {str(e)}", self)
    
    def exportar_clientes(self):
        try:
            ruta_archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar Clientes como CSV", 
                f"clientes_{datetime.now().strftime('%Y%m%d')}.csv",
                "Archivos CSV (*.csv)"
            )
            
            if ruta_archivo:
                Reportes.exportar_clientes_csv(ruta_archivo)
                Mensajes.mostrar_exito(f"Clientes exportados correctamente a:\n{ruta_archivo}", self)
        
        except Exception as e:
            Mensajes.mostrar_error(f"Error al exportar clientes: {str(e)}", self)
    
    def generar_reporte_ventas(self):
        try:
            fecha_inicio = self.fecha_inicio.date().toString('yyyy-MM-dd')
            fecha_fin = self.fecha_fin.date().toString('yyyy-MM-dd')
            
            reporte = Reportes.generar_reporte_ventas_por_periodo(fecha_inicio, fecha_fin)
            
            # Mostrar estadísticas
            estadisticas = reporte['estadisticas']
            mensaje = f"""
            Reporte de Ventas ({fecha_inicio} a {fecha_fin})
            
            Total de Ventas: {estadisticas['total_ventas']}
            Ingresos Totales: ${estadisticas['ingresos_totales']:,.2f}
            Promedio por Venta: ${estadisticas['promedio_venta']:,.2f}
            Venta Mínima: ${estadisticas['venta_minima']:,.2f}
            Venta Máxima: ${estadisticas['venta_maxima']:,.2f}
            """
            
            # Mostrar productos populares en tabla
            self.mostrar_productos_populares(reporte['productos_populares'])
            
            Mensajes.mostrar_exito(mensaje, self)
        
        except Exception as e:
            Mensajes.mostrar_error(f"Error al generar reporte: {str(e)}", self)
    
    def generar_reporte_stock(self):
        try:
            reporte = Reportes.generar_reporte_stock()
            
            # Mostrar productos con stock bajo
            stock_bajo = reporte['stock_bajo']
            if stock_bajo:
                self.mostrar_stock_bajo(stock_bajo)
                
                mensaje = f"""
                Reporte de Stock
                
                Productos con stock bajo: {len(stock_bajo)}
                Valor total del inventario: ${reporte['valor_inventario']:,.2f}
                
                Se recomienda reabastecer los productos marcados.
                """
            else:
                mensaje = f"""
                Reporte de Stock
                
                ¡Excelente! No hay productos con stock bajo.
                Valor total del inventario: ${reporte['valor_inventario']:,.2f}
                """
            
            Mensajes.mostrar_exito(mensaje, self)
        
        except Exception as e:
            Mensajes.mostrar_error(f"Error al generar reporte: {str(e)}", self)
    
    def mostrar_productos_populares(self, productos):
        self.table_resultados.setColumnCount(4)
        self.table_resultados.setHorizontalHeaderLabels([
            "Producto", "Cantidad Vendida", "Ingresos", "Promedio por Unidad"
        ])
        
        self.table_resultados.setRowCount(len(productos))
        
        for row, producto in enumerate(productos):
            self.table_resultados.setItem(row, 0, QTableWidgetItem(producto[0]))
            self.table_resultados.setItem(row, 1, QTableWidgetItem(str(producto[1])))
            self.table_resultados.setItem(row, 2, QTableWidgetItem(f"${producto[2]:.2f}"))
            promedio = producto[2] / producto[1] if producto[1] > 0 else 0
            self.table_resultados.setItem(row, 3, QTableWidgetItem(f"${promedio:.2f}"))
        
        header = self.table_resultados.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def mostrar_stock_bajo(self, productos):
        self.table_resultados.setColumnCount(4)
        self.table_resultados.setHorizontalHeaderLabels([
            "Producto", "Stock Actual", "Stock Mínimo", "Unidad"
        ])
        
        self.table_resultados.setRowCount(len(productos))
        
        for row, producto in enumerate(productos):
            self.table_resultados.setItem(row, 0, QTableWidgetItem(producto[0]))
            
            stock_item = QTableWidgetItem(str(producto[1]))
            if producto[1] == 0:
                stock_item.setBackground(Qt.GlobalColor.red)
                stock_item.setForeground(Qt.GlobalColor.white)
            elif producto[1] < producto[2]:
                stock_item.setBackground(Qt.GlobalColor.yellow)
            self.table_resultados.setItem(row, 1, stock_item)
            
            self.table_resultados.setItem(row, 2, QTableWidgetItem(str(producto[2])))
            self.table_resultados.setItem(row, 3, QTableWidgetItem(producto[3]))
        
        header = self.table_resultados.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)