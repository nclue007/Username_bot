import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توكن البوت
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"{APP_URL}{WEBHOOK_PATH}"

PATTERNS = {
    "1": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
    "2": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6)),
    "3": lambda: 'user_' + ''.join(random.choices('0123456789', k=4))
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل /generate <نمط> للحصول على اسم مستخدم.\nالأنماط: 1، 2، 3")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        pattern = context.args[0]
        if pattern in PATTERNS:
            username = PATTERNS[pattern]()
            await update.message.reply_text(f"الاسم المقترح: {username}")
        else:
            await update.message.reply_text("النمط غير معروف. استخدم 1 أو 2 أو 3.")
    else:
        await update.message.reply_text("يرجى تحديد النمط بعد الأمر.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    PORT = int(os.environ.get("PORT", 8443))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
