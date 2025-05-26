#!/bin/bash
echo "🛑 Deteniendo servidor Django, Ngrok, Celery Y servicio systemd..."

# 1. Detener el servicio systemd (si está activo)
if sudo systemctl is-active --quiet mi_servidor.service; then
    echo "▸ Deteniendo mi_servidor.service..."
    sudo systemctl stop mi_servidor.service
fi

# 2. Matar procesos manuales (por si se iniciaron sin systemd)
echo "▸ Matando procesos restantes..."
pkill -f "manage.py runserver"
pkill -f "ngrok"
pkill -f "celery"

# 3. Verificación final
if pgrep -f "manage.py runserver" || pgrep -f "ngrok" || pgrep -f "celery"; then
    echo "⚠️ Algunos procesos no se detuvieron. Forzando cierre..."
    pkill -9 -f "manage.py runserver"
    pkill -9 -f "ngrok"
    pkill -9 -f "celery"
fi

echo "✅ Todo detenido (servicio + procesos manuales)."
