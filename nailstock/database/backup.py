import shutil
from datetime import datetime
from pathlib import Path

def crear_respaldo(ruta_destino=None):
    """
    Crea un respaldo de la base de datos principal.

    - Si no se especifica `ruta_destino`, crea un archivo dentro de la carpeta
      `backups/` con un nombre que incluye la fecha y hora actual.
    - Si se pasa `ruta_destino`, guarda el respaldo exactamente en esa ruta.

    :param ruta_destino: Ruta completa donde se guardará el respaldo (opcional).
    :return: Ruta final del archivo de respaldo creado.
    :raises FileNotFoundError: Si la base de datos original no existe.
    """
    # Ruta de la base de datos principal de la aplicación
    db_path = Path("database/nailstock.db")

    if not db_path.exists():
        # Si la base de datos no existe, no tiene sentido crear un respaldo
        raise FileNotFoundError("La base de datos no existe")

    if ruta_destino is None:
        # Generar un nombre de archivo con timestamp para evitar sobrescribir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_destino = f"backups/nailstock_backup_{timestamp}.db"

    # Crear la carpeta de destino si no existe (ej. "backups/")
    Path(ruta_destino).parent.mkdir(parents=True, exist_ok=True)

    # Crear copia de la base de datos (copy2 conserva metadata del archivo)
    shutil.copy2(db_path, ruta_destino)

    return ruta_destino

def restaurar_respaldo(ruta_respaldo):
    """
    Restaura la base de datos a partir de un archivo de respaldo.

    Pasos que realiza:
    1. Verifica que el archivo de respaldo exista.
    2. Crea un respaldo de la base de datos actual antes de restaurar
       (por seguridad, por si la restauración sale mal).
    3. Copia el archivo de respaldo sobre la base de datos principal.

    :param ruta_respaldo: Ruta del archivo de respaldo a usar para la restauración.
    :return: True si la restauración se realizó sin errores.
    :raises FileNotFoundError: Si el archivo de respaldo no existe.
    """
    # Ruta de la base de datos principal
    db_path = Path("database/nailstock.db")

    if not Path(ruta_respaldo).exists():
        # No se encontró el archivo de respaldo indicado
        raise FileNotFoundError("El archivo de respaldo no existe")

    # Antes de modificar la base de datos actual, crear un respaldo de seguridad
    crear_respaldo(f"backups/pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

    # Sobrescribir la base de datos con el respaldo elegido
    shutil.copy2(ruta_respaldo, db_path)

    return True