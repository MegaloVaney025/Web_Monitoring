import requests
from logger_module import logger

def send_teams_message(message: str, webhook_url: str):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        logger.info("✅ Mensaje enviado a Teams")
    else:
        logger.error(f"❌ Error {response.status_code} al enviar a Teams: {response.text}")
