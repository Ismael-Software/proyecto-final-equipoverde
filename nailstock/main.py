import os
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

import sys
from PyQt6.QtWidgets import QApplication
from database.db_connection import DBConnection
from views.login_view import LoginView
from views.main_window import MainWindow

class NailStackApp:
    def __init__(self):
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("NailStack")
            self.app.setApplicationVersion("1.0.0")
            self.app.setOrganizationName("Ferretería NailStack")
            self.db_connection = DBConnection()
            
    def show_login(self):
        self.login_view = LoginView(self.on_login_success)
        self.login_view.show()

    def on_login_success(self):
        self.login_view.close()
        self.main_window = MainWindow()
        self.main_window.show()
    
    def run(self):
        self.show_login()
        return self.app.exec()

if __name__ == '__main__':
    nailstack = NailStackApp()
    sys.exit(nailstack.run())
