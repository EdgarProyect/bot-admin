import os
import json
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, JobQueue
)
from bienvenida import enviar_bienvenida
from schedule_ads import schedule_ads
from grupos_utils import cargar_grupos, guardar_grupo_si_nuevo, mostrar_grupos

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_ID", "7475229565").split(",")]

# Configuración de logs
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text("¡Hola! Soy EDBot. 🤖")

async def grupos_cmd(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ No estás autorizado para usar este comando.")
        return
    grupos = cargar_grupos()
    texto = "📋 Grupos registrados:\n" + "\n".join([f"• {g}" for g in grupos])
    await update.message.reply_text(texto)

async def handle_new_members(update, context):
    guardar_grupo_si_nuevo(update.effective_chat.id)
    await enviar_bienvenida(update, context)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grupos", grupos_cmd))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_members))

    schedule_ads(app.job_queue)

    logger.info("🤖 EDBot en marcha")
    await app.run_polling()

# === ESTA ES LA CLAVE PARA EVITAR EL ERROR ===
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
