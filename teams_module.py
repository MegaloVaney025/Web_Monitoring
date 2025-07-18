import requests

def send_teams_message(message: str, webhook_url: str):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("✅ Mensaje enviado a Teams")
    else:
        print(f"❌ Error {response.status_code} al enviar a Teams: {response.text}")
