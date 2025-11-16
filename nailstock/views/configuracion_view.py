from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QGroupBox, QMessageBox,
                             QFormLayout, QLineEdit)
from PyQt6.QtCore import QProcess
from database.backup import crear_respaldo, restaurar_respaldo
from utils.mensajes import Mensajes
import os
import sys
import subprocess

class ConfiguracionView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Sección de respaldo y restauración
        backup_group = QGroupBox("Respaldo y Restauración")
        backup_layout = QVBoxLayout()
        
        # Botón para crear respaldo
        backup_btn_layout = QHBoxLayout()
        btn_respaldo = QPushButton("Crear Respaldo")
        self.respaldo_label = QLabel("")
        
        btn_respaldo.clicked.connect(self.crear_respaldo)
        
        backup_btn_layout.addWidget(btn_respaldo)
        backup_btn_layout.addWidget(self.respaldo_label)
        backup_btn_layout.addStretch()
        
        # Botón para restaurar respaldo
        restore_btn_layout = QHBoxLayout()
        btn_restore = QPushButton("Restaurar desde Respaldo")
        btn_restore.clicked.connect(self.restaurar_respaldo)
        
        restore_btn_layout.addWidget(btn_restore)
        restore_btn_layout.addStretch()
        
        # Botón para abrir carpeta de respaldos
        open_folder_layout = QHBoxLayout()
        btn_open_folder = QPushButton("Abrir carpeta de respaldos")
        btn_open_folder.clicked.connect(self.abrir_carpeta_respaldos)
        
        open_folder_layout.addWidget(btn_open_folder)
        open_folder_layout.addStretch()
        
        backup_layout.addLayout(backup_btn_layout)
        backup_layout.addLayout(restore_btn_layout)
        backup_layout.addLayout(open_folder_layout)
        backup_group.setLayout(backup_layout)
        
        # Sección de configuración general
        config_group = QGroupBox("Configuración General")
        config_layout = QFormLayout()
        
        self.nombre_ferreteria = QLineEdit()
        self.nombre_ferreteria.setPlaceholderText("Nombre de la ferretería")
        
        self.telefono_ferreteria = QLineEdit()
        self.telefono_ferreteria.setPlaceholderText("Teléfono de contacto")
        
        self.direccion_ferreteria = QLineEdit()
        self.direccion_ferreteria.setPlaceholderText("Dirección")
        
        btn_guardar_config = QPushButton("Guardar Configuración")
        btn_guardar_config.clicked.connect(self.guardar_configuracion)
        
        config_layout.addRow("Nombre:", self.nombre_ferreteria)
        config_layout.addRow("Teléfono:", self.telefono_ferreteria)
        config_layout.addRow("Dirección:", self.direccion_ferreteria)
        config_layout.addRow(btn_guardar_config)
        config_group.setLayout(config_layout)
        
        # Sección de información del sistema
        info_group = QGroupBox("Información del Sistema")
        info_layout = QFormLayout()
        
        info_layout.addRow("Versión:", QLabel("NailStack 1.0.0"))
        info_layout.addRow("Base de Datos:", QLabel("SQLite"))
        info_layout.addRow("Desarrollado con:", QLabel("Python 3.13.2 + PyQt6"))
        
        info_group.setLayout(info_layout)
        
        layout.addWidget(backup_group)
        layout.addWidget(config_group)
        layout.addWidget(info_group)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def crear_respaldo(self):
        try:
            ruta_archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar Respaldo", 
                f"respaldo_nailstack_{self.get_timestamp()}.db",
                "Archivos de Base de Datos (*.db)"
            )
            
            if ruta_archivo:
                ruta_final = crear_respaldo(ruta_archivo)
                self.respaldo_label.setText(f"Respaldo creado: {os.path.basename(ruta_final)}")
                Mensajes.mostrar_exito("Respaldo creado con éxito.", self)
        
        except Exception as e:
            Mensajes.mostrar_error(f"No se pudo crear el respaldo: {str(e)}", self)
    
    def restaurar_respaldo(self):
        try:
            ruta_archivo, _ = QFileDialog.getOpenFileName(
                self, "Seleccionar Archivo de Respaldo", 
                "", "Archivos de Base de Datos (*.db)"
            )
            
            if ruta_archivo:
                if Mensajes.confirmar("¿Deseas restaurar este respaldo?", self):
                    restaurar_respaldo(ruta_archivo)
                    Mensajes.mostrar_exito(
                        "Base de datos restaurada correctamente.\n"
                        "La aplicación se reiniciará para aplicar los cambios.", 
                        self
                    )
                    self.reiniciar_aplicacion()
        
        except Exception as e:
            Mensajes.mostrar_error(f"No se pudo restaurar el respaldo: {str(e)}", self)
    
    def abrir_carpeta_respaldos(self):
        try:
            # Obtener el directorio actual de trabajo
            directorio_actual = os.getcwd()
            
            # Intentar abrir la carpeta según el sistema operativo
            if sys.platform == "win32":
                os.startfile(directorio_actual)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", directorio_actual])
            else:  # Linux y otros
                subprocess.run(["xdg-open", directorio_actual])
                
        except Exception as e:
            Mensajes.mostrar_error(f"No se pudo abrir la carpeta: {str(e)}", self)
    
    def reiniciar_aplicacion(self):
        """Reinicia la aplicación después de restaurar un respaldo"""
        QProcess.startDetached(sys.executable, sys.argv)
        sys.exit()
    
    def guardar_configuracion(self):
        # Aquí iría la lógica para guardar la configuración
        Mensajes.mostrar_exito("Configuración guardada correctamente", self)
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")