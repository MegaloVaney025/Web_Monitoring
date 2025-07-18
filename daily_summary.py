import datetime
import pytz
from telegram_module import send_telegram_message
from logger_module import logger

class DailySummary:
    def __init__(self):
        self.daily_alerts = 0
        self.daily_recoveries = 0
        self.last_summary_date = None
        self.timezone = pytz.timezone('America/Mexico_City')
        self.target_hour = 18

    def increment_alerts(self):
        """Thread-safe alert counter increment."""
        self.daily_alerts += 1

    def increment_recoveries(self):
        """Thread-safe recovery counter increment."""
        self.daily_recoveries += 1

    def _should_send_summary(self) -> bool:
        """Determine if it's time to send the daily summary."""
        try:
            now = datetime.datetime.now(self.timezone)
            target_time = now.replace(
                hour=self.target_hour,
                minute=0,
                second=0,
                microsecond=0
            )

            # Conditions for sending:
            # 1. First run (initialize last_summary_date)
            # 2. Current time is at/past 6 PM AND we haven't sent today
            if self.last_summary_date is None:
                self.last_summary_date = now.date()
                return False

            return now >= target_time and self.last_summary_date < now.date()

        except Exception as e:
            logger.error(f"Error checking summary time: {e}")
            return False

    def _generate_message(self) -> str:
        """Create the formatted summary message."""
        return (
            "📊 Resumen diario de monitoreo (6 PM GMT-6):\n"
            f"• Alertas hoy: {self.daily_alerts}\n"
            f"• Recuperaciones hoy: {self.daily_recoveries}\n"
            f"• Hora de reporte: {datetime.datetime.now(self.timezone).strftime('%H:%M %Z')}"
        )

    def try_send_summary(self) -> bool:
        try:
            if not self._should_send_summary():
                return False

            message = self._generate_message()
            if send_telegram_message(message):  # Assume returns True on success
                self._reset_counters()
                logger.info("✅ Daily summary sent successfully")
                return True
            else:
                logger.warning("⚠️ Failed to send Telegram daily summary")
                return False

        except Exception as e:
            logger.error(f"❌ Critical error in daily summary: {e}", exc_info=True)
            return False