# daily_summary_test.py
import time
import datetime
from daily_summary import DailySummary

def fake_send_telegram_message(msg):
    print(f"[Telegram mock] Mensaje enviado:\n{msg}")

# Reemplazamos la función real con el mock para test
from daily_summary import send_telegram_message
daily_summary_instance = DailySummary()
daily_summary_instance.send_telegram_message = fake_send_telegram_message

def test_daily_summary():
    ds = DailySummary()
    
    # Simulamos incrementos de alertas y recuperaciones
    ds.increment_alerts()
    ds.increment_alerts()
    ds.increment_recoveries()

    # Primer intento no envía mensaje (es primer arranque)
    ds.try_send_summary()
    print("Primer try_send_summary ejecutado (no debe enviar mensaje)")

    # Forzamos cambio de día simulando fecha pasada
    ds.last_summary_date = ds.last_summary_date.replace(day=ds.last_summary_date.day - 1)

    # Ahora sí debe enviar mensaje
    ds.try_send_summary()
    print("Segundo try_send_summary ejecutado (debe enviar mensaje y resetear contadores)")

    # Verificamos que contadores se resetearon
    assert ds.daily_alerts == 0, "daily_alerts no se reinició"
    assert ds.daily_recoveries == 0, "daily_recoveries no se reinició"
    print("Contadores reiniciados correctamente")

if __name__ == "__main__":
    test_daily_summary()
