# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta donde está config.py
SCREENSHOTS_BASE_DIR = os.path.join(BASE_DIR, "screenshots")
LOGS_BASE_DIR = os.path.join(BASE_DIR, "logs")

# Clientes y su configuración individual
CLIENTS = {
    "Chantilly": {
        "urls": ["https://www.grupochantilly.com.mx"],
        "teams_webhook": os.getenv("TEAMS_WEBHOOK_CHANTILLY"), # <- From .env
        "log_dir": os.path.join(LOGS_BASE_DIR, "Chantilly"),
        "screenshot_dir": os.path.join(SCREENSHOTS_BASE_DIR, "Chantilly"),
    },
    "ICIntracom": {
        "urls": ["https://www.icintracom.com.mx/nosotros"],
        "log_dir": os.path.join(LOGS_BASE_DIR, "ICIntracom"),
        "teams_webhook": os.getenv("TEAMS_WEBHOOK_ICINTRACOM"), # <- From .env
        "screenshot_dir": os.path.join(SCREENSHOTS_BASE_DIR, "ICIntracom"),
    },
}

# Config general (No sensible)
NORMAL_CHECK_INTERVAL = 900  # segundos
ALERT_CHECK_INTERVAL = 60
SSL_ALERT_DAYS = 7

# Telegram (From .env)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")