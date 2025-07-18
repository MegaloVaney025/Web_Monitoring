import requests
import ssl
import socket
from datetime import datetime
from config import SSL_ALERT_DAYS, ACCEPTABLE_STATUS_CODES

def check_url_status(url: str, ssl_alert_days = SSL_ALERT_DAYS) -> dict:
    """
    Verifica el estado de la URL y el certificado SSL.

    :param url: URL a verificar
    :param ssl_alert_days: días antes de vencimiento para alertar
    :return: diccionario con resultados
    """
    result = {
        "url": url,
        "up": False,
        "status_code": None,
        "timeout": False,
        "ssl_expired": False,
        "ssl_expiring_soon": False,
        "error": None,
    }

    # Verificar status HTTP
    try:
        response = requests.get(url, timeout=10)
        result["status_code"] = response.status_code
        result["up"] = response.status_code in ACCEPTABLE_STATUS_CODES
    except requests.Timeout:
        result["timeout"] = True
        result["error"] = "Timeout"
        return result
    except requests.RequestException as e:
        result["error"] = str(e)
        return result

    # Verificar SSL si es HTTPS
    if url.startswith("https://"):
        hostname = url.split("//")[1].split("/")[0].split(":")[0]  # Ignores port
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    exp_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (exp_date - datetime.utcnow()).days
                    if days_left < 0:
                        result["ssl_expired"] = True
                    elif days_left < ssl_alert_days:
                        result["ssl_expiring_soon"] = True
        except Exception as e:
            result["error"] = f"SSL check failed: {e}"

    return result