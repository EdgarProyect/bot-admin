# C:\dev\bots\b1\idgroup.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN  "7916605053:AAEdfx4Vup-A-Afgy1bhYJhdFbkY-tegca8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Usa /groupinfo en un grupo para obtener y guardar su nombre e ID."
    )

async def groupinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        msg = f"Nombre: {chat.title} | ID: {chat.id}"
        await update.message.reply_text(msg)
        with open("group_info.txt", "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        print(f"✅ Guardado en group_info.txt: {msg}")
    else:
        await update.message.reply_text("Esto solo funciona en grupos o supergrupos.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("groupinfo", groupinfo))

    print("🤖 Bot corriendo... envía /groupinfo en tus grupos para ir guardando la info.")
    app.run_polling()  # 🔹 ya no usamos asyncio.run()

if __name__ == "__main__":
    main()
