from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QComboBox, QSpinBox,
                             QHeaderView, QMessageBox, QLabel)
from ..models.cliente_model import ClienteModel
from ..models.producto_model import ProductoModel
from ..controllers.venta_controller import VentaController
from ..utils.mensajes import Mensajes

class VentasView(QWidget):
    def __init__(self):
        super().__init__()
        self.productos_venta = []
        self.init_ui()
        self.cargar_clientes()
        self.cargar_productos()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Selección de cliente
        cliente_layout = QHBoxLayout()
        cliente_layout.addWidget(QLabel("Cliente:"))
        self.cliente_combo = QComboBox()
        self.cliente_combo.setFixedWidth(300)
        cliente_layout.addWidget(self.cliente_combo)
        cliente_layout.addStretch()
        
        # Tabla de productos en venta
        self.table_venta = QTableWidget()
        self.table_venta.setColumnCount(6)
        self.table_venta.setHorizontalHeaderLabels([
            "ID", "Producto", "Precio Unitario", "Cantidad", "Subtotal", "Acciones"
        ])
        
        header = self.table_venta.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # Total
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(QLabel("Total:"))
        self.total_label = QLabel("$0.00")
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        total_layout.addWidget(self.total_label)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_agregar_producto = QPushButton("Agregar Producto")
        self.btn_agregar_producto.clicked.connect(self.mostrar_dialogo_productos)

        self.btn_registrar_venta = QPushButton("Registrar Venta")
        self.btn_registrar_venta.clicked.connect(self.registrar_venta)
        self.btn_registrar_venta.setStyleSheet("background-color: #27ae60; color: white;")

        btn_layout.addWidget(self.btn_agregar_producto)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_registrar_venta)

        layout.addLayout(cliente_layout)
        layout.addWidget(QLabel("Productos en la venta:"))
        layout.addWidget(self.table_venta)
        layout.addLayout(total_layout)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.actualizar_total()

    def cargar_clientes(self):
        clientes = ClienteModel.obtener_clientes()
        self.cliente_combo.clear()
        self.cliente_combo.addItem("Seleccionar cliente...", None)
        for cliente in clientes:
            self.cliente_combo.addItem(cliente[1], cliente[0])

    def cargar_productos(self):
        self.productos = ProductoModel.obtener_productos()

    def mostrar_dialogo_productos(self):
        dialog = SeleccionProductoDialog(self, self.productos)
        if dialog.exec():
            producto_data = dialog.get_selected_producto()
            self.agregar_producto_venta(producto_data)

    def agregar_producto_venta(self, producto_data):
        # Verificar si el producto ya está en la venta
        for i, prod in enumerate(self.productos_venta):
            if prod['producto_id'] == producto_data['producto_id']:
                # Actualizar cantidad
                self.productos_venta[i]['cantidad'] += producto_data['cantidad']
                self.productos_venta[i]['subtotal'] = (
                        self.productos_venta[i]['cantidad'] * self.productos_venta[i]['precio_unitario']
                )
                self.actualizar_tabla_venta()
                return

        # Agregar nuevo producto
        self.productos_venta.append(producto_data)
        self.actualizar_tabla_venta()

    def actualizar_tabla_venta(self):
        self.table_venta.setRowCount(len(self.productos_venta))

        for row, producto in enumerate(self.productos_venta):
            self.table_venta.setItem(row, 0, QTableWidgetItem(str(producto['producto_id'])))
            self.table_venta.setItem(row, 1, QTableWidgetItem(producto['nombre']))
            self.table_venta.setItem(row, 2, QTableWidgetItem(f"${producto['precio_unitario']:.2f}"))

            # Cantidad editable
            spin_cantidad = QSpinBox()
            spin_cantidad.setMinimum(1)
            spin_cantidad.setMaximum(999)
            spin_cantidad.setValue(producto['cantidad'])
            spin_cantidad.valueChanged.connect(
                lambda value, r=row: self.actualizar_cantidad(r, value)
            )
            self.table_venta.setCellWidget(row, 3, spin_cantidad)

            self.table_venta.setItem(row, 4, QTableWidgetItem(f"${producto['subtotal']:.2f}"))

            # Botón eliminar
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda checked, r=row: self.eliminar_producto_venta(r))
            self.table_venta.setCellWidget(row, 5, btn_eliminar)

        self.actualizar_total()

    def actualizar_cantidad(self, row, cantidad):
        if 0 <= row < len(self.productos_venta):
            self.productos_venta[row]['cantidad'] = cantidad
            self.productos_venta[row]['subtotal'] = (
                    cantidad * self.productos_venta[row]['precio_unitario']
            )
            self.actualizar_tabla_venta()

    def eliminar_producto_venta(self, row):
        if 0 <= row < len(self.productos_venta):
            self.productos_venta.pop(row)
            self.actualizar_tabla_venta()

    def actualizar_total(self):
        total = sum(prod['subtotal'] for prod in self.productos_venta)
        self.total_label.setText(f"${total:.2f}")

    def registrar_venta(self):
        cliente_id = self.cliente_combo.currentData()

        if not cliente_id:
            Mensajes.mostrar_error("Debe seleccionar un cliente", self)
            return

        if not self.productos_venta:
            Mensajes.mostrar_error("Debe agregar al menos un producto a la venta", self)
            return

        try:
            venta_id = VentaController.registrar_venta(
                cliente_id, self.productos_venta
            )

            Mensajes.mostrar_exito(f"Venta registrada correctamente. ID: {venta_id}", self)

            # Limpiar venta
            self.productos_venta.clear()
            self.actualizar_tabla_venta()
            self.cliente_combo.setCurrentIndex(0)

        except Exception as e:
            Mensajes.mostrar_error(str(e), self)


class SeleccionProductoDialog(QMessageBox):
    def __init__(self, parent, productos):
        super().__init__(parent)
        self.productos = productos
        self.selected_producto = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Seleccionar Producto")

        # Crear un widget personalizado para la selección
        widget = QWidget()
        layout = QVBoxLayout()

        # Combo de productos
        self.producto_combo = QComboBox()
        for producto in self.productos:
            if producto[6] > 0:  # Solo productos con stock
                text = f"{producto[1]} - ${producto[5]:.2f} (Stock: {producto[6]})"
                self.producto_combo.addItem(text, producto[0])

        # Cantidad
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setMaximum(1000)

        # Botones
        btn_layout = QHBoxLayout()
        btn_aceptar = QPushButton("Aceptar")
        btn_cancelar = QPushButton("Cancelar")

        btn_aceptar.clicked.connect(self.aceptar)
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_aceptar)
        btn_layout.addWidget(btn_cancelar)

        layout.addWidget(QLabel("Producto:"))
        layout.addWidget(self.producto_combo)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_spin)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        self.layout().addWidget(widget, 0, 0)

    def aceptar(self):
        producto_id = self.producto_combo.currentData()
        cantidad = self.cantidad_spin.value()

        if producto_id:
            # Buscar producto seleccionado
            for producto in self.productos:
                if producto[0] == producto_id:
                    self.selected_producto = {
                        'producto_id': producto_id,
                        'nombre': producto[1],
                        'precio_unitario': producto[5],
                        'cantidad': cantidad,
                        'subtotal': cantidad * producto[5]
                    }
                    break
            
            self.accept()
    
    def get_selected_producto(self):
        return self.selected_producto
