#!/usr/bin/env python3

import requests
import socket

TOKEN = "7512055988:AAF3pQ7kAlxf63O_9PsUQITqfmwzqYgEgiw"
CHAT_ID = "5481766894"

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = 'No se pudo obtener la IP'
    finally:
        s.close()
    return ip_local

def enviar_mensaje(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensaje}
    requests.post(url, data=data)

if __name__ == "__main__":
    ip = obtener_ip_local()
    enviar_mensaje(f"🚀 Raspberry iniciada\n🔗 IP local: http://{ip}")
