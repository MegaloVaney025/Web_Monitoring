def get_alert_messages(status: dict) -> dict:
    """
    Recibe el dict de estado de una URL y devuelve mensajes para Teams y Telegram.

    :param status: diccionario con resultado de check_url_status()
    :return: dict con mensajes para 'teams' y 'telegram'
    """
    url = status.get("url")
    up = status.get("up")
    timeout = status.get("timeout")
    ssl_expired = status.get("ssl_expired")
    ssl_expiring_soon = status.get("ssl_expiring_soon")
    status_code = status.get("status_code")
    error = status.get("error")

    if timeout:
        msg = f"⏰ Timeout detectado en {url}"
    elif not up:
        if error:
            msg = f"❌ Página caída en {url}. Error: {error}"
        else:
            msg = f"❌ Página caída en {url} (Código HTTP {status_code})"
    elif ssl_expired:
        msg = f"⚠️ Certificado SSL expirado en {url}"
    elif ssl_expiring_soon:
        msg = f"⚠️ Certificado SSL por vencer pronto en {url}"
    else:
        msg = f"✅ {url} está UP y funcionando correctamente."

    return {
        "teams": msg,
        "telegram": msg,
    }
