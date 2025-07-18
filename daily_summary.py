# daily_summary.py
import datetime
from telegram_module import send_telegram_message

class DailySummary:
    def __init__(self):
        self.last_summary_date = None
        self.daily_alerts = 0
        self.daily_recoveries = 0

    def increment_alerts(self):
        self.daily_alerts += 1

    def increment_recoveries(self):
        self.daily_recoveries += 1

    def try_send_summary(self):
        now = datetime.datetime.now()
        if self.last_summary_date is None:
            self.last_summary_date = now.date()
            return  # No enviar resumen en el arranque inicial

        if now.date() != self.last_summary_date:
            msg = (f"📊 Resumen diario de monitoreo:\n"
                   f"Alertas hoy: {self.daily_alerts}\n"
                   f"Recuperaciones hoy: {self.daily_recoveries}\n")
            send_telegram_message(msg)
            self.daily_alerts = 0
            self.daily_recoveries = 0
            self.last_summary_date = now.date()