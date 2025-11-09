from PyQt6.QtWidgets import QMessageBox

class Mensajes:
    @staticmethod
    def mostrar_error(mensaje, parent=None):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(mensaje)
        msg.exec()
    
    @staticmethod
    def mostrar_exito(mensaje, parent=None):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Éxito")
        msg.setText(mensaje)
        msg.exec()
    
    @staticmethod
    def mostrar_advertencia(mensaje, parent=None):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText(mensaje)
        msg.exec()
    
    @staticmethod
    def confirmar(mensaje, parent=None):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirmar")
        msg.setText(mensaje)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return msg.exec() == QMessageBox.StandardButton.Yes