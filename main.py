from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random, os

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{os.getenv('RENDER_EXTERNAL_URL')}{WEBHOOK_PATH}"

# أنماط أسماء المستخدمين
PATTERNS = {
    "1": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
    "2": lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6)),
    "3": lambda: 'user_' + ''.join(random.choices('0123456789', k=4))
}

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("أرسل /generate <نمط> للحصول على اسم مستخدم.\nالأنماط: 1، 2، 3")

# أمر /generate
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

# الدالة الرئيسية
async def main():
    app = Application.builder().token(TOKEN).build()

    # إضافة الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    # إعداد Webhook
    await app.bot.delete_webhook()
    await app.bot.set_webhook(WEBHOOK_URL)

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        path=WEBHOOK_PATH
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

  
