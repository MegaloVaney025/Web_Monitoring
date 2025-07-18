from config import CLIENTS
from teams_module import send_teams_message

cliente = "Chantilly"
msg = f"Esto es una prueba de mensaje Teams para {cliente} el cual se implementará para monitoreo 24/7 de la página web, favor de omitir este mensaje."

webhook = CLIENTS[cliente]["teams_webhook"]

send_teams_message(msg, webhook)
