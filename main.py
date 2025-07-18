import time
from web_checker import check_url_status
from logger_module import log_status
from messages import get_alert_messages
from teams_module import send_teams_message
from telegram_module import send_telegram_message
from screenshot_manager import enviar_y_borrar_screenshots
import config
from daily_summary import DailySummary

# Diccionario para guardar estado de alerta por cliente y url
alert_mode = {}

def is_alert_mode(client, url):
    return alert_mode.get(client, {}).get(url, False)

def set_alert_mode(client, url, value: bool):
    if client not in alert_mode:
        alert_mode[client] = {}
    alert_mode[client][url] = value

daily_summary = DailySummary()

def main_loop():
    print("Monitor iniciado exitosamente", flush = True)
    normal_interval = config.NORMAL_CHECK_INTERVAL
    alert_interval = config.ALERT_CHECK_INTERVAL
    ssl_alert_days = config.SSL_ALERT_DAYS

    while True:
        for client, conf in config.CLIENTS.items():
            urls = conf["urls"]
            log_dir = conf["log_dir"]
            webhook = conf["teams_webhook"]

            for url in urls:
                status = check_url_status(url, ssl_alert_days)
                
                # Loggear el estado
                log_status(client, log_dir, status)

                # Determinar si hay un fallo
                is_down = not status["up"] or status["timeout"] or status["ssl_expired"] or status["ssl_expiring_soon"]
                currently_alert = is_alert_mode(client, url)

                if is_down and not currently_alert:
                    # Entramos en modo alerta
                    set_alert_mode(client, url, True)
                    daily_summary.increment_alerts()
                    msgs = get_alert_messages(status)
                    send_teams_message(msgs["teams"], webhook)
                    send_telegram_message(msgs["telegram"])
                    print(f"🔴 ALERTA ACTIVADA para {client} - {url}")

                elif not is_down and currently_alert:
                    # Recuperación
                    set_alert_mode(client, url, False)
                    daily_summary.increment_recoveries()
                    recovery_msg = f"✅ RECUPERACIÓN: {url} está UP nuevamente."
                    send_teams_message(recovery_msg, webhook)
                    send_telegram_message(recovery_msg)
                    enviar_y_borrar_screenshots(client, conf["screenshot_dir"], url)
                    print(f"🟢 ALERTA FINALIZADA para {client} - {url}")

                elif is_down and currently_alert:
                    # Seguimos en modo alerta (solo Telegram)
                    msgs = get_alert_messages(status)
                    send_telegram_message(msgs["telegram"])
                    print(f"🔴 ALERTA CONTINÚA para {client} - {url}")

                else:
                    # Estado normal, sin alertas
                    print(f"🟢 {client} - {url} está UP")

        # Intentar enviar resumen diario
        daily_summary.try_send_summary()

        # Determinar el intervalo de sleep
        interval = alert_interval if any(
            is_alert_mode(client, url)
            for client in alert_mode
            for url in alert_mode[client]
        ) else normal_interval

        print(f"Sleeping {interval} seconds...\n")
        time.sleep(interval)

if __name__ == "__main__":
    main_loop()
