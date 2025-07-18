import os
from screenshot_module import take_screenshot
from telegram_module import send_telegram_photo
from logger_module import logger

def enviar_y_borrar_screenshots(client_name: str, screenshot_dir: str, url: str):
    """
    Envía todas las capturas de la carpeta screenshot_dir relacionadas con url y cliente,
    y las borra tras enviarlas correctamente.
    """
    files = [f for f in os.listdir(screenshot_dir) if f.endswith(".png") and url.replace("https://", "").replace("/", "_") in f]

    for filename in files:
        full_path = os.path.join(screenshot_dir, filename)
        caption = f"Evidencia para {client_name} - {url}\nArchivo: {filename}"
        success = send_telegram_photo(full_path, caption)
        if success:
            os.remove(full_path)
            logger.info(f"🗑️ Archivo borrado: {filename}")
        else:
            logger.warning(f"⚠️ No se borró {filename} porque no se envió correctamente")