from messages import get_alert_messages
from teams_module import send_teams_message
from telegram_module import send_telegram_message  # importa tu módulo correcto
import config

if __name__ == "__main__":
    test_status = {
        "url": "https://example.com",
        "up": False,
        "timeout": False,
        "ssl_expired": False,
        "ssl_expiring_soon": False,
        "status_code": 503,
        "error": None,
    }

    msgs = get_alert_messages(test_status)

    # Webhook Teams por cliente
    webhook = config.CLIENTS["Chantilly"]["teams_webhook"]

    send_teams_message(msgs["teams"], webhook)
    send_telegram_message(msgs["telegram"])  # SOLO el mensaje, nada más

