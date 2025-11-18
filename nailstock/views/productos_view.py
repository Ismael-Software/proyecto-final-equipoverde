from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
                             QHeaderView, QDialog, QFormLayout, 
                             QSpinBox, QDoubleSpinBox, QLabel)
from PyQt6.QtCore import Qt
from ..models.producto_model import ProductoModel
from ..models.proveedor_model import ProveedorModel
from ..controllers.producto_controller import ProductoController
from ..utils.mensajes import Mensajes

class ProductosView(QWidget):
    def __init__(self):
        super().__init__()
        self.productos = []
        self.proveedores = []
        self.init_ui()
        self.cargar_productos()
        self.cargar_proveedores()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Barra de búsqueda y filtros
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.textChanged.connect(self.buscar_productos)
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItem("Todas las categorías", "")
        self.categoria_combo.currentIndexChanged.connect(self.filtrar_productos)
        
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(QLabel("Categoría:"))
        search_layout.addWidget(self.categoria_combo)
        search_layout.addStretch()
        
        # Botones
        btn_agregar = QPushButton("Agregar Producto")
        btn_agregar.clicked.connect(self.agregar_producto)
        
        search_layout.addWidget(btn_agregar)
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoría", "Proveedor", "Precio Compra", 
            "Precio Venta", "Stock", "Unidad", "Acciones"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def cargar_productos(self):
        try:
            self.productos = ProductoModel.obtener_productos()
            self.actualizar_tabla(self.productos)
            
            # Actualizar categorías
            categorias = set()
            for producto in self.productos:
                categoria = producto[3] if producto[3] else "Sin categoría"
                categorias.add(categoria)
            
            self.categoria_combo.clear()
            self.categoria_combo.addItem("Todas las categorías", "")
            for categoria in sorted(categorias):
                self.categoria_combo.addItem(categoria, categoria)
                
        except Exception as e:
            Mensajes.mostrar_error(f"Error cargando productos: {str(e)}", self)
    
    def cargar_proveedores(self):
        try:
            self.proveedores = ProveedorModel.obtener_proveedores()
        except Exception as e:
            Mensajes.mostrar_error(f"Error cargando proveedores: {str(e)}", self)
    
    def buscar_productos(self):
        termino = self.search_input.text().strip()
        if termino:
            try:
                productos = ProductoModel.buscar_productos(termino)
                self.actualizar_tabla(productos)
            except Exception as e:
                Mensajes.mostrar_error(f"Error buscando productos: {str(e)}", self)
        else:
            self.actualizar_tabla(self.productos)
    
    def filtrar_productos(self):
        categoria = self.categoria_combo.currentData()
        if categoria:
            productos_filtrados = [p for p in self.productos if p[3] == categoria]
            self.actualizar_tabla(productos_filtrados)
        else:
            self.actualizar_tabla(self.productos)
    
    def actualizar_tabla(self, productos):
        try:
            self.table.setRowCount(len(productos))
            
            for row, producto in enumerate(productos):
                self.table.setItem(row, 0, QTableWidgetItem(str(producto[0])))
                self.table.setItem(row, 1, QTableWidgetItem(producto[1]))
                self.table.setItem(row, 2, QTableWidgetItem(producto[3] or "Sin categoría"))
                self.table.setItem(row, 3, QTableWidgetItem(producto[12] or "Sin proveedor"))
                self.table.setItem(row, 4, QTableWidgetItem(f"${producto[4]:.2f}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"${producto[5]:.2f}"))
                
                # Stock
                stock_item = QTableWidgetItem(str(producto[6]))
                if producto[6] <= producto[7]:  # stock <= stock_minimo
                    stock_item.setBackground(Qt.GlobalColor.red)
                    stock_item.setForeground(Qt.GlobalColor.white)
                self.table.setItem(row, 6, stock_item)
                
                self.table.setItem(row, 7, QTableWidgetItem(producto[8]))
                
                # Acciones
                actions_widget = QWidget()
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(0, 0, 0, 0)
                
                btn_editar = QPushButton("Editar")
                btn_editar.clicked.connect(lambda checked, p=producto: self.editar_producto(p))
                
                btn_eliminar = QPushButton("Eliminar")
                btn_eliminar.clicked.connect(lambda checked, p=producto: self.eliminar_producto(p))
                
                actions_layout.addWidget(btn_editar)
                actions_layout.addWidget(btn_eliminar)
                actions_widget.setLayout(actions_layout)
                
                self.table.setCellWidget(row, 8, actions_widget)
                
        except Exception as e:
            Mensajes.mostrar_error(f"Error actualizando tabla: {str(e)}", self)

    def agregar_producto(self):
        dialog = ProductoDialog(self, self.proveedores)
        if dialog.exec():
            self.cargar_productos()
    
    def editar_producto(self, producto):
        dialog = ProductoDialog(self, self.proveedores, producto)
        if dialog.exec():
            self.cargar_productos()
    
    def eliminar_producto(self, producto):
        if Mensajes.confirmar(f"¿Está seguro de eliminar el producto {producto[1]}?", self):
            try:
                ProductoModel.eliminar_producto(producto[0])
                Mensajes.mostrar_exito("Producto eliminado correctamente", self)
                self.cargar_productos()
            except Exception as e:
                Mensajes.mostrar_error(str(e), self)

class ProductoDialog(QDialog):
    def __init__(self, parent=None, proveedores=None, producto=None):
        super().__init__(parent)
        self.producto = producto
        self.proveedores = proveedores
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Editar Producto" if self.producto else "Agregar Producto")
        self.setModal(True)
        
        layout = QFormLayout()
        
        # Campos
        self.nombre_input = QLineEdit()
        self.descripcion_input = QLineEdit()
        self.categoria_input = QLineEdit()
        
        self.precio_compra_input = QDoubleSpinBox()
        self.precio_compra_input.setMaximum(999999.99)
        self.precio_compra_input.setPrefix("$ ")
        
        self.precio_venta_input = QDoubleSpinBox()
        self.precio_venta_input.setMaximum(999999.99)
        self.precio_venta_input.setPrefix("$ ")
        
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(999999)
        
        self.stock_minimo_input = QSpinBox()
        self.stock_minimo_input.setMaximum(999999)
        
        self.unidad_input = QLineEdit()
        self.unidad_input.setPlaceholderText("pz, kg, m, etc.")
        
        self.proveedor_combo = QComboBox()
        self.proveedor_combo.addItem("Sin proveedor", None)
        for proveedor in self.proveedores:
            self.proveedor_combo.addItem(proveedor[1], proveedor[0])
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        
        btn_guardar.clicked.connect(self.guardar)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        
        # Agregar campos al layout
        layout.addRow("Nombre *:", self.nombre_input)
        layout.addRow("Descripción:", self.descripcion_input)
        layout.addRow("Categoría:", self.categoria_input)
        layout.addRow("Precio Compra *:", self.precio_compra_input)
        layout.addRow("Precio Venta *:", self.precio_venta_input)
        layout.addRow("Stock *:", self.stock_input)
        layout.addRow("Stock Mínimo:", self.stock_minimo_input)
        layout.addRow("Unidad *:", self.unidad_input)
        layout.addRow("Proveedor:", self.proveedor_combo)
        layout.addRow(btn_layout)
        
        # Cargar datos si es edición
        if self.producto:
            self.nombre_input.setText(self.producto[1])
            self.descripcion_input.setText(self.producto[2] or "")
            self.categoria_input.setText(self.producto[3] or "")
            self.precio_compra_input.setValue(self.producto[4])
            self.precio_venta_input.setValue(self.producto[5])
            self.stock_input.setValue(self.producto[6])
            self.stock_minimo_input.setValue(self.producto[7])
            self.unidad_input.setText(self.producto[8])
            
            # Seleccionar proveedor
            index = self.proveedor_combo.findData(self.producto[9])
            if index >= 0:
                self.proveedor_combo.setCurrentIndex(index)
        
        self.setLayout(layout)
    
    def guardar(self):
        try:
            data = {
                'nombre': self.nombre_input.text().strip(),
                'descripcion': self.descripcion_input.text().strip(),
                'categoria': self.categoria_input.text().strip(),
                'precio_compra': self.precio_compra_input.value(),
                'precio_venta': self.precio_venta_input.value(),
                'stock': self.stock_input.value(),
                'stock_minimo': self.stock_minimo_input.value(),
                'unidad': self.unidad_input.text().strip(),
                'proveedor_id': self.proveedor_combo.currentData()
            }
            
            if self.producto:
                ProductoController.actualizar_producto(self.producto[0], **data)
                Mensajes.mostrar_exito("Producto actualizado correctamente", self)
            else:
                ProductoController.agregar_producto(**data)
                Mensajes.mostrar_exito("Producto agregado correctamente", self)
            
            self.accept()
            
        except Exception as e:
            Mensajes.mostrar_error(str(e), self)