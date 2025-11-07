import sqlite3
from pathlib import Path

class DBConnection:
    def __init__(self):
        self.db_path = Path("database/nailstack.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
    
    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def _create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            script_path = Path(__file__).parent / "create_tables.sql"
            with open(script_path, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
            

_db_connection = DBConnection()

def get_db_connection():
    return _db_connection.get_connection()