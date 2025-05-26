#!/bin/bash

# === RUTAS ===
PROYECTO_DIR="/home/$USER/Documents/inventario-elconet"
ENTORNO_VIRTUAL="$PROYECTO_DIR/env/bin/activate"
NGROK_BIN="/usr/local/bin/ngrok"

# === VARIABLES DEL BOT ===
BOT_TOKEN="7512055988:AAF3pQ7kAlxf63O_9PsUQITqfmwzqYgEgiw"
CHAT_ID=-4985420036
WEBHOOK_ENDPOINT="/productos/webhook/"

# === FUNCIÓN PARA OBTENER IP LOCAL ===
get_local_ip() {
    hostname -I | awk '{print $1}'
}

# === FUNCIÓN PARA ENVIAR MENSAJE A TELEGRAM ===
send_telegram_msg() {
    local ip="$1"
    local msg="🚀 Servidor Django iniciado correctamente%0A🔗 IP local: http://${ip}:8000"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        -d "text=${msg}" \
        -d "disable_notification=false"
}

# === INICIO DEL SCRIPT ===

# PASO 1: Activar entorno y ejecutar Django
cd "$PROYECTO_DIR"
source "$ENTORNO_VIRTUAL"
python manage.py runserver 0.0.0.0:8000 &
sleep 2

# PASO 2: Ejecutar ngrok
deactivate
"$NGROK_BIN" http 8000 > /dev/null &
sleep 5

# PASO 3: Configurar webhook
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9.-]*\.ngrok-free\.app' | head -n 1)

if [ -z "$NGROK_URL" ]; then
  echo "❌ No se pudo obtener la URL pública de ngrok. Verifica que ngrok esté instalado y activo."
  exit 1
fi

FULL_WEBHOOK="${NGROK_URL}${WEBHOOK_ENDPOINT}"
echo "🌐 Webhook completo: $FULL_WEBHOOK"

# PASO 4: Enviar webhook a Telegram
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" -d "url=${FULL_WEBHOOK}"

# PASO 5: Iniciar Celery
cd "$PROYECTO_DIR"
source "$ENTORNO_VIRTUAL"
celery -A inventario worker -l info &

# === ENVÍO DE NOTIFICACIÓN FINAL ===
LOCAL_IP=$(get_local_ip)
send_telegram_msg "$LOCAL_IP"

echo "✅ Servidor iniciado. Notificación enviada a Telegram."
