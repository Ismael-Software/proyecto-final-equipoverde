from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from views.productos_view import ProductosView
from views.proveedores_view import ProveedoresView
from views.clientes_view import ClientesView
from views.ventas_view import VentasView
from views.reportes_view import ReportesView
from views.configuracion_view import ConfiguracionView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
  
    def init_ui(self):
        self.setWindowTitle(f"NailStack - Sistema de Gestión [Usuario: Administrador.]")
        self.setGeometry(100, 100, 1200, 700)
      
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
      
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
      
        # Panel lateral
        side_panel = QFrame()
        side_panel.setFixedWidth(200)
        side_panel.setStyleSheet("background-color: #2c3e50; color: white;")
      
        side_layout = QVBoxLayout()
        side_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
      
        # Título del panel
        title_label = QLabel("NAILSTACK")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("padding: 20px; color: #3498db;")
      
        # Botones de navegación
        self.btn_productos = self.crear_boton_menu("Productos")
        self.btn_proveedores = self.crear_boton_menu("Proveedores")
        self.btn_clientes = self.crear_boton_menu("Clientes")
        self.btn_ventas = self.crear_boton_menu("Ventas")
        self.btn_reportes = self.crear_boton_menu("Reportes")
        self.btn_configuracion = self.crear_boton_menu("Configuración")
      
        # Conectar botones
        self.btn_productos.clicked.connect(lambda: self.cambiar_vista(0))
        self.btn_proveedores.clicked.connect(lambda: self.cambiar_vista(1))
        self.btn_clientes.clicked.connect(lambda: self.cambiar_vista(2))
        self.btn_ventas.clicked.connect(lambda: self.cambiar_vista(3))
        self.btn_reportes.clicked.connect(lambda: self.cambiar_vista(4))
        self.btn_configuracion.clicked.connect(lambda: self.cambiar_vista(5))
      
        # Agregar al layout lateral
        side_layout.addWidget(title_label)
        side_layout.addWidget(self.btn_productos)
        side_layout.addWidget(self.btn_proveedores)
        side_layout.addWidget(self.btn_clientes)
        side_layout.addWidget(self.btn_ventas)
        side_layout.addWidget(self.btn_reportes)
        side_layout.addWidget(self.btn_configuracion)
      
        side_panel.setLayout(side_layout)
      
        # Área de contenido
        self.stacked_widget = QStackedWidget()
      
        # Crear vistas
        self.vistas = [
            ProductosView(),
            ProveedoresView(),
            ClientesView(),
            VentasView(),
            ReportesView(),
            ConfiguracionView()
        ]
      
        for vista in self.vistas:
            self.stacked_widget.addWidget(vista)
      
        # Agregar al layout principal
        main_layout.addWidget(side_panel)
        main_layout.addWidget(self.stacked_widget)
      
        # Mostrar primera vista
        self.cambiar_vista(0)
  
    def crear_boton_menu(self, texto):
        btn = QPushButton(texto)
        btn.setFixedHeight(40)
        btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        ''')
        return btn
  
    def cambiar_vista(self, index):
        self.stacked_widget.setCurrentIndex(index)
      
        # Resetear estilos de todos los botones
        for btn in [self.btn_productos, self.btn_proveedores, self.btn_clientes,
                   self.btn_ventas, self.btn_reportes, self.btn_configuracion]:
            btn.setStyleSheet('''
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: white;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            ''')
      
        # Resaltar botón activo
        botones = [self.btn_productos, self.btn_proveedores, self.btn_clientes,
                  self.btn_ventas, self.btn_reportes, self.btn_configuracion]

        botones[index].setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
            }
        ''')