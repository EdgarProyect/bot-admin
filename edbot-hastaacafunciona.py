import os
import json
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# 🌱 Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# 📦 Estado global
grupos = {}

# 📋 Logger setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("ads")

# 🧠 Función para cargar los grupos desde el JSON
def cargar_grupos():
    global grupos
    if os.path.exists("grupos.json"):
        with open("grupos.json", "r", encoding="utf-8") as f:
            grupos = json.load(f)
        logger.info(f"✅ Grupos cargados correctamente: {len(grupos)} grupos.")
    else:
        grupos = {}
        logger.warning("⚠️ 'grupos.json' no encontrado. Inicializando grupos vacíos.")

# 💾 Guardar grupos en archivo
def guardar_grupos():
    with open("grupos.json", "w", encoding="utf-8") as f:
        json.dump(grupos, f, ensure_ascii=False, indent=2)
    logger.info("💾 Grupos guardados.")

# 📍 Comando /grupos
async def listar_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ No estás autorizado para ver esta información.")

    if not grupos:
        return await update.message.reply_text("📭 No estoy en ningún grupo.")

    texto = "📋 *Grupos activos:*\n\n"
    for group_id, info in grupos.items():
        nombre = info.get("title", "Nombre desconocido")
        tipo = info.get("type", "¿?")
        texto += f"• {nombre}\n  ID: `{group_id}`\n  Tipo: `{tipo}`\n\n"

    logger.info(f"👤 Admin {ADMIN_ID} pidió /grupos. Total: {len(grupos)} grupos.")
    return await update.message.reply_markdown_v2(texto)

# 🧪 Función que simula registrar un grupo (puede ya estar en tu bot real)
async def join_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        grupos[str(chat.id)] = {
            "title": chat.title,
            "type": chat.type,
        }
        guardar_grupos()
        await update.message.reply_text(f"✅ Me uní a {chat.title} y lo registré.")
        logger.info(f"🚀 Registrado grupo nuevo: {chat.title} ({chat.id})")

# 🔁 Job de ejemplo si usás schedule_ads
async def schedule_ads(context: ContextTypes.DEFAULT_TYPE):
    logger.info("📢 Ejecutando job de anuncios...")
    # lógica de anuncios automáticos

# 🧠 Main async
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("grupos", listar_grupos))
    app.add_handler(CommandHandler("registrar", join_group))  # comando para probar registro

    # Si tenés anuncios programados
    if app.job_queue:
        app.job_queue.run_repeating(schedule_ads, interval=1800, first=10)
    else:
        logger.warning("⚠️ JobQueue no inicializado. Instalá con: pip install 'python-telegram-bot[job-queue]'")

    logger.info("🤖 Bot en marcha...")
    await app.run_polling()

# 🟢 Iniciar: Carga grupos y ejecuta

from telegram.ext import ApplicationBuilder
import asyncio

# ------------------ BOT ENTRY POINT ------------------
if __name__ == '__main__':
    import sys

    try:
        # Crear app
        app = ApplicationBuilder().token(TOKEN).build()

        # Registrar handlers
        app.add_handler(CommandHandler("grupos", listar_grupos))
        app.add_handler(CommandHandler("registrar", join_group))

        # Si usás JobQueue
        if app.job_queue:
            app.job_queue.run_repeating(schedule_ads, interval=1800, first=10)
        else:
            logger.warning("⚠️ JobQueue no inicializado. Instalá con: pip install 'python-telegram-bot[job-queue]'")

        logger.info("🤖 Bot en marcha...")
        app.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        print(f"❌ Error al iniciar el bot: {e}", file=sys.stderr)



