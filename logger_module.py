# logger_module.py
import logging
import os
from config import LOGS_BASE_DIR

# Crear directorio de logs si no existe
if not os.path.exists(LOGS_BASE_DIR):
    os.makedirs(LOGS_BASE_DIR)

# Configurar logger global
logger = logging.getLogger("web_monitor")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Handler para archivo general
file_handler = logging.FileHandler(os.path.join(LOGS_BASE_DIR, "monitor.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
