from config import CLIENTS
from logger_module import log_status

# Simula resultado de check_url_status
data = {
    "url": "https://example.com",
    "status_code": 200,
    "up": True,
    "timeout": False,
    "ssl_expired": False,
    "ssl_expiring_soon": False,
    "error": None
}

client = "Chantilly"
log_dir = CLIENTS[client]["log_dir"]

log_status(client, log_dir, data)