import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import sys
from asgiref.sync import sync_to_async

# Añade la raíz del proyecto al path (un nivel arriba del actual)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ajusta el nombre del módulo a tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')

import django
django.setup()

from django.conf import settings
from productos.models import Producto
from django.db.models import F

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comando /stock
async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Uso correcto: /stock <código>")
        return

    codigo = context.args[0]
    try:
        producto = await sync_to_async(Producto.objects.get)(codigo=codigo)
        mensaje = f"📦`{producto.codigo}` - *{producto.nombre}*\nStock actual: `{producto.cantidad}` unidades"
    except Producto.DoesNotExist:
        mensaje = f"❌ Producto con código `{codigo}` no encontrado."

    await update.message.reply_text(mensaje, parse_mode="Markdown")

# Comando /alertas
async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    productos = await sync_to_async(
        lambda: list(Producto.objects.filter(alerta_activa=True, cantidad__lte=F("alerta_stock")))
    )()

    if productos:
        mensaje = "*📉 Productos en alerta de stock:*\n"
        for p in productos:
            mensaje += (f"- `{p.codigo}` - {p.nombre}: `{p.cantidad}` unidades\n"
                        f"*Stock recomendado*: `{p.alerta_stock}` unidades\n\n")
    else:
        mensaje = "✅ No hay productos en alerta de stock."

    await update.message.reply_text(mensaje, parse_mode="Markdown")

# Ejecutar bot en modo polling
def main():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("stock", stock))
    application.add_handler(CommandHandler("alertas", alertas))

    logger.info("Bot iniciado en modo polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
