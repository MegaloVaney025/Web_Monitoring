import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message: str) -> bool:
    """
    Envía un mensaje a tu chat de Telegram.

    :param message: texto a enviar
    :return: True si se envió exitosamente, False si hubo error
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()
        print("✅ Mensaje enviado a Telegram")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al enviar mensaje a Telegram: {e}")
        return False

def send_telegram_photo(photo_path: str, caption: str = "") -> bool:
    """
    Envía una foto con caption a Telegram.

    :param photo_path: ruta local del archivo de imagen
    :param caption: texto descriptivo
    :return: True si éxito, False si falla
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        with open(photo_path, "rb") as photo_file:
            files = {"photo": photo_file}
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            response = requests.post(url, data=data, files=files, timeout=10)
            response.raise_for_status()
        print(f"✅ Foto enviada a Telegram: {photo_path}")
        return True
    except Exception as e:
        print(f"❌ Error enviando foto a Telegram: {e}")
        return False