from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QMessageBox
)
import sys


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NailStock - Inicio de Sesión")
        self.setGeometry(400, 200, 300, 200)
        self.init_ui()

    def init_ui(self):
        self.label_usuario = QLabel("Usuario:")
        self.label_contrasena = QLabel("Contraseña:")

        self.input_usuario = QLineEdit()
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón para iniciar sesion
        self.btn_iniciar = QPushButton("Iniciar sesión")
        self.btn_iniciar.clicked.connect(self.verificar_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.label_contrasena)
        layout.addWidget(self.input_contrasena)
        layout.addWidget(self.btn_iniciar)

        self.setLayout(layout)

    def verificar_login(self):
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()

        if usuario == "admin" and contrasena == "1234":
            QMessageBox.information(self, "Éxito", "Inicio de sesión correcto")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")


