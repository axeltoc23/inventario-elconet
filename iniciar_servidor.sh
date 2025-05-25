#!/bin/bash

# === RUTAS ===
PROYECTO_DIR="/home/$USER/Documents/inventario-elconet"
ENTORNO_VIRTUAL="$PROYECTO_DIR/env/bin/activate"
NGROK_BIN="/usr/local/bin/ngrok"  # Asegúrate de que ngrok esté instalado aquí

# === VARIABLES DEL BOT ===
BOT_TOKEN="7512055988:AAF3pQ7kAlxf63O_9PsUQITqfmwzqYgEgiw"
WEBHOOK_ENDPOINT="/productos/webhook/"

# === PASO 1: Activar entorno y ejecutar Django ===
cd "$PROYECTO_DIR"
source "$ENTORNO_VIRTUAL"
python manage.py runserver 0.0.0.0:8000 &
sleep 2

# === PASO 2: Ejecutar ngrok (fuera del entorno virtual) ===
deactivate  # salimos del entorno virtual
"$NGROK_BIN" http 8000 > /dev/null &
sleep 5  # Esperamos que arranque ngrok y cree el túnel

# === PASO 3: Obtener URL pública de ngrok ===
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9.-]*\.ngrok-free\.app' | head -n 1)

if [ -z "$NGROK_URL" ]; then
  echo "❌ No se pudo obtener la URL pública de ngrok. Verifica que ngrok esté instalado y activo."
  exit 1
fi

FULL_WEBHOOK="${NGROK_URL}${WEBHOOK_ENDPOINT}"
echo "🌐 Webhook completo: $FULL_WEBHOOK"

# === PASO 4: Enviar Webhook a Telegram ===
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" -d "url=${FULL_WEBHOOK}"

# === PASO 5: Volver a entorno virtual y lanzar Celery ===
cd "$PROYECTO_DIR"
source "$ENTORNO_VIRTUAL"
celery -A inventario worker -l info &
