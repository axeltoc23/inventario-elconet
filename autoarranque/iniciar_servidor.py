#!/usr/bin/env python3
import subprocess
import time
import logging

logging.basicConfig(
    filename='/tmp/mi_servidor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def run_servidor():
    try:
        logging.info("Ejecutando script Bash original...")
        # Ejecuta tu script .sh SIN MODIFICARLO
        subprocess.Popen(
            ["/bin/bash", "/home/axel/Documents/inventario-elconet/iniciar_servidor.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        logging.info("Servicios lanzados. Manteniendo proceso activo...")
        while True:  # Bucle infinito para evitar que el servicio se cierre
            time.sleep(60)  # Reduce carga de CPU
            
    except Exception as e:
        logging.error(f"Error crítico: {str(e)}")

if __name__ == "__main__":
    run_servidor()
