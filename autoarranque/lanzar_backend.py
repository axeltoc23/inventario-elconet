#!/usr/bin/env python3
import subprocess
import time
import logging
import requests

LOG_FILE = "/tmp/lanzar_backend.log"
SCRIPT_BASH = "/home/axel/Documents/inventario-elconet/iniciar_servidor.sh"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def verificar_conexion_internet(reintentos=10, espera=5):
    for intento in range(reintentos):
        try:
            requests.get("https://8.8.8.8", timeout=3)
            logging.info("✅ Conexión a internet verificada.")
            return True
        except Exception:
            logging.warning(f"⏳ [{intento+1}/{reintentos}] Sin conexión. Esperando {espera}s...")
            time.sleep(espera)
    return False

def ejecutar_script_bash():
    try:
        logging.info(f"🚀 Ejecutando script: {SCRIPT_BASH}")
        proceso = subprocess.Popen(
            ["/bin/bash", SCRIPT_BASH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info("✅ Script lanzado exitosamente.")
        return proceso
    except Exception as e:
        logging.error(f"❌ Error al lanzar el script: {e}")
        return None

if __name__ == "__main__":
    logging.info("📦 Arranque del servicio iniciado.")
    if verificar_conexion_internet():
        proceso = ejecutar_script_bash()
        if proceso:
            while True:
                time.sleep(60)
        else:
            logging.error("❌ No se pudo iniciar el script. Saliendo.")
    else:
        logging.error("❌ No hay conexión a internet. Abortando inicio.")
