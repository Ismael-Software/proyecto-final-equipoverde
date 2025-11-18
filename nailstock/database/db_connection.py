import sqlite3
from pathlib import Path
import os
import sys

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")  

    return os.path.join(base_path, relative_path)


class DBConnection:
    def __init__(self):
        self.db_path = Path("database/nailstock.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
    
    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def _create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            sql_file_path = resource_path("create_tables.sql")

            if not os.path.exists(sql_file_path):
                return

            with open(sql_file_path, "r", encoding="utf-8") as f:
                script = f.read()

            cursor.executescript(script)
            conn.commit()


# Instancia global
_db_connection = DBConnection()

def get_db_connection():
    return _db_connection.get_connection()
