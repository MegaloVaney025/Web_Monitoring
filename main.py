import time
import signal
import sys

from web_checker import check_url_status
from status_logger_module import log_status
from messages import get_alert_messages
from teams_module import send_teams_message
from telegram_module import send_telegram_message
from screenshot_manager import enviar_y_borrar_screenshots
import config
from daily_summary import DailySummary
from logger_module import logger

# Estado global de alerta
alert_mode = {}

# Inicializar resumen diario
daily_summary = DailySummary()

def is_alert_mode(client, url):
    return alert_mode.get(client, {}).get(url, False)

def set_alert_mode(client, url, value: bool):
    if client not in alert_mode:
        alert_mode[client] = {}
    alert_mode[client][url] = value

def clean_alert_mode(clients_config):
    """Eliminar clientes o urls huérfanas de alert_mode."""
    existing_clients = set(clients_config.keys())
    for client in list(alert_mode.keys()):
        if client not in existing_clients:
            del alert_mode[client]
        else:
            existing_urls = set(clients_config[client]["urls"])
            for url in list(alert_mode[client].keys()):
                if url not in existing_urls:
                    del alert_mode[client][url]

def process_url(client, conf, url, ssl_alert_days):
    """Procesa el chequeo, logging y alertas de una URL específica."""
    try:
        status = check_url_status(url, ssl_alert_days)
    except Exception as e:
        logger.error(f"[ERROR] Fallo al checar {client} - {url}: {e}")
        return

    log_dir = conf["log_dir"]
    webhook = conf["teams_webhook"]

    try:
        log_status(client, log_dir, status)
    except Exception as e:
        logger.error(f"[ERROR] Fallo al loggear {client} - {url}: {e}")

    is_down = not status["up"] or status["timeout"] or status["ssl_expired"] or status["ssl_expiring_soon"]
    currently_alert = is_alert_mode(client, url)

    try:
        if is_down and not currently_alert:
            # Activar alerta
            set_alert_mode(client, url, True)
            daily_summary.increment_alerts()
            msgs = get_alert_messages(status)
            send_teams_message(msgs["teams"], webhook)
            send_telegram_message(msgs["telegram"])
            logger.info(f"🔴 ALERTA ACTIVADA para {client} - {url}")

        elif not is_down and currently_alert:
            # Recuperación
            set_alert_mode(client, url, False)
            daily_summary.increment_recoveries()
            recovery_msg = f"✅ RECUPERACIÓN: {url} está UP nuevamente."
            send_teams_message(recovery_msg, webhook)
            send_telegram_message(recovery_msg)
            enviar_y_borrar_screenshots(client, conf["screenshot_dir"], url)
            logger.info(f"🟢 ALERTA FINALIZADA para {client} - {url}")

        elif is_down and currently_alert:
            # Alerta continua (solo Telegram)
            msgs = get_alert_messages(status)
            send_telegram_message(msgs["telegram"])
            logger.info(f"🔴 ALERTA CONTINÚA para {client} - {url}")

        else:
            # Estado normal
            logger.info(f"🟢 {client} - {url} está UP")

    except Exception as e:
        logger.error(f"[ERROR] Fallo en proceso de alertas para {client} - {url}: {e}")

def graceful_shutdown(sig, frame):
    logger.info("🛑 Recibida señal de salida. Cerrando monitor...")
    sys.exit(0)

def main_loop():
    logger.info("Monitor iniciado exitosamente")
    normal_interval = config.NORMAL_CHECK_INTERVAL
    alert_interval = config.ALERT_CHECK_INTERVAL
    ssl_alert_days = config.SSL_ALERT_DAYS

    # Configurar graceful shutdown
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    while True:
        clean_alert_mode(config.CLIENTS)

        for client, conf in config.CLIENTS.items():
            urls = conf["urls"]
            for url in urls:
                process_url(client, conf, url, ssl_alert_days)

        # Intentar enviar resumen diario
        try:
            daily_summary.try_send_summary()
        except Exception as e:
            logger.error(f"[ERROR] Fallo al enviar resumen diario: {e}")

        # Determinar el intervalo de sleep
        interval = alert_interval if any(
            is_alert_mode(client, url)
            for client in alert_mode
            for url in alert_mode[client]
        ) else normal_interval

        logger.info(f"Sleeping for {interval} seconds...")

        # Contador regresivo en tiempo real
        for remaining in range(interval, 0, -1):
            mins, secs = divmod(remaining, 60)
            timeformat = f"{mins:02d}:{secs:02d}"
            logger.info(f"\r⏳ Next check in {timeformat}", end='')
            time.sleep(1)

        logger.info("\n")  # Salto de línea después de contador

if __name__ == "__main__":
    main_loop()
