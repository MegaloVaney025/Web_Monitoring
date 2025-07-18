from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
from logger_module import logger

def take_screenshot(client_name: str, screenshot_dir: str, url: str):
    """
    Toma screenshot de la URL y lo guarda en screenshot_dir con timestamp.
    """
    # Configura Selenium en modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.set_page_load_timeout(15)
        driver.get(url)
    except Exception as e:
        logger.warning(f"⚠️ Error al cargar la página para screenshot: {e}")

    # Asegura carpeta
    os.makedirs(screenshot_dir, exist_ok=True)

    # Nombre del archivo
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    file_name = f"{client_name}_{safe_url}_{timestamp}.png"
    file_path = os.path.join(screenshot_dir, file_name)

    # Guarda screenshot
    driver.save_screenshot(file_path)
    logger.info(f"📸 Screenshot guardado: {file_path}")

    driver.quit()
    return file_path