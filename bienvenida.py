import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def enviar_bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia mensaje de bienvenida cuando un nuevo usuario se une al grupo"""
    for usuario in update.message.new_chat_members:
        nombre = usuario.first_name
        chat = update.effective_chat.title
        mensaje = (
            f"👋 ¡Bienvenido/a {nombre} al grupo *{chat}*!\n"
            "Por favor, leé las reglas 📜 y compartí contenido de valor 💬.\n\n"
            "✅ Si estás de acuerdo, quedate y participá.\n"
            "🚫 Si no, el grupo es libre... ¡pero con respeto!"
        )
        try:
            await update.effective_chat.send_message(
                text=mensaje,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"❌ Error enviando bienvenida: {e}")

