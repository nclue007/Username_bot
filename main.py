
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random, os

TOKEN = os.getenv("BOT_TOKEN")

# نماذج لأسماء المستخدمين
PATTERNS = {
    "1": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
    "2": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6)),
    "3": lambda: 'user_' + ''.join(random.choices('0123456789', k=4))
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("أرسل /generate <نمط> للحصول على اسم مستخدم.
الأنماط: 1، 2، 3")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    app.run_polling()

if __name__ == "__main__":
    main()
