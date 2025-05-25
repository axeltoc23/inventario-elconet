#!/bin/bash
echo "🛑 Deteniendo servidor Django, ngrok y Celery..."
pkill -f "manage.py runserver"
pkill -f "ngrok"
pkill -f "celery"
echo "✅ Todo detenido."
