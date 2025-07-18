import csv
import os
from datetime import datetime, timezone
from threading import Lock
from logger_module import logger  # Importar logger global

_log_lock = Lock()

def log_status(client_name: str, log_dir: str, data: dict):
    """
    Guarda el status de una página en un CSV por cliente y loggea la operación.

    :param client_name: nombre del cliente
    :param log_dir: carpeta específica de logs de este cliente
    :param data: diccionario con los resultados de check_url_status
    """
    try:
        with _log_lock:
            # Asegura que la carpeta exista
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Define el archivo de log
            log_file = os.path.join(log_dir, f"{client_name}_status_log.csv")

            # Checa si el archivo ya existe para saber si escribir encabezados
            file_exists = os.path.isfile(log_file)

            with open(log_file, mode="a", newline='', encoding="utf-8") as csvfile:
                fieldnames = [
                    "timestamp",
                    "url",
                    "status_code",
                    "up",
                    "timeout",
                    "ssl_expired",
                    "ssl_expiring_soon",
                    "error",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Escribe encabezados si el archivo no existía antes
                if not file_exists:
                    writer.writeheader()

                # Escribe la fila con los datos actuales
                writer.writerow({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "url": data.get("url"),
                    "status_code": data.get("status_code"),
                    "up": data.get("up"),
                    "timeout": data.get("timeout"),
                    "ssl_expired": data.get("ssl_expired"),
                    "ssl_expiring_soon": data.get("ssl_expiring_soon"),
                    "error": data.get("error"),
                })

            logger.info(f"Logged status for {client_name} - {data.get('url')} with status_code {data.get('status_code')}")
    except Exception as e:
        logger.error(f"Error logging status for {client_name} - {data.get('url')}: {e}", exc_info=True)
