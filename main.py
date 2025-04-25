import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# بيانات البوت
TOKEN = "YOUR_BOT_TOKEN"

LANGUAGES = {
    'ar': 'العربية 🇸🇦',
    'en': 'English 🇬🇧',
    'fr': 'Français 🇫🇷',
    'es': 'Español 🇪🇸',
    'de': 'Deutsch 🇩🇪',
    'ru': 'Русский 🇷🇺',
    'zh': '中文 🇨🇳',
    'ja': '日本語 🇯🇵',
    'hi': 'हिन्दी 🇮🇳',
    'pt': 'Português 🇵🇹',
    'tr': 'Türkçe 🇹🇷',
    'it': 'Italiano 🇮🇹',
    'ko': '한국어 🇰🇷',
    'fa': 'فارسی 🇮🇷',
    'ur': 'اردو 🇵🇰',
    'bn': 'বাংলা 🇧🇩',
    'vi': 'Tiếng Việt 🇻🇳',
    'th': 'ไทย 🇹🇭',
    'id': 'Bahasa Indonesia 🇮🇩',
    'nl': 'Nederlands 🇳🇱',
    'pl': 'Polski 🇵🇱',
    'uk': 'Українська 🇺🇦'
}

USERNAME_STYLES = {
    'style1': 'A_B_C (20 نجمة)',
    'style2': 'a_b_c (20 نجمة)',
    'style3': 'ABC12 (مجاني)',
    'style4': 'A_B_9 (17 نجمة)',
    'style5': 'a_B_9 (17 نجمة)',
    'style6': 'a_9_9 (17 نجمة)',
    'style7': 'A_9_9 (17 نجمة)'
}

user_data = {}

def generate_username(style_id):
    if style_id == 'style1':
        return '_'.join([random.choice(string.ascii_uppercase) for _ in range(3)])
    elif style_id == 'style2':
        return '_'.join([random.choice(string.ascii_lowercase) for _ in range(3)])
    elif style_id == 'style3':
        chars = random.choices(string.ascii_uppercase, k=3)
        nums = random.choices(string.digits, k=2)
        random.shuffle(chars + nums)
        return ''.join(chars + nums)
    elif style_id == 'style4':
        return f"{random.choice(string.ascii_uppercase)}_{random.choice(string.ascii_uppercase)}_{random.choice(string.digits)}"
    elif style_id == 'style5':
        return f"{random.choice(string.ascii_lowercase)}_{random.choice(string.ascii_uppercase)}_{random.choice(string.digits)}"
    elif style_id == 'style6':
        return f"{random.choice(string.ascii_lowercase)}_{random.choice(string.digits)}_{random.choice(string.digits)}"
    elif style_id == 'style7':
        return f"{random.choice(string.ascii_uppercase)}_{random.choice(string.digits)}_{random.choice(string.digits)}"
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def start(update: Update, context: CallbackContext):
    keyboard = []
    langs = list(LANGUAGES.items())
    for i in range(0, len(langs), 3):
        row = [InlineKeyboardButton(name, callback_data=f'lang_{code}') for code, name in langs[i:i+3]]
        keyboard.append(row)
    update.message.reply_text("اختر اللغة / Choose language:", reply_markup=InlineKeyboardMarkup(keyboard))

def language_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    lang = query.data.split('_')[1]
    user_id = query.from_user.id
    user_data[user_id] = {
        'lang': lang,
        'stars': 30,
        'used_usernames': [],
        'paid_styles': set()
    }
    show_styles(query, user_id)

def show_styles(query, user_id):
    lang = user_data[user_id]['lang']
    keyboard = []
    styles = list(USERNAME_STYLES.items())
    for i in range(0, len(styles), 2):
        row = []
        for j in range(2):
            if i + j < len(styles):
                key, label = styles[i + j]
                lock = ""
                if key not in ['style3'] and key not in user_data[user_id]['paid_styles']:
                    required = 20 if key in ['style1', 'style2'] else 17
                    if user_data[user_id]['stars'] >= required:
                        user_data[user_id]['paid_styles'].add(key)
                    else:
                        lock = " 🔒"
                row.append(InlineKeyboardButton(label + lock, callback_data=f'style_{key}'))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(f"رصيد النجوم: {user_data[user_id]['stars']} ⭐", callback_data='show_stars')])
    keyboard.append([InlineKeyboardButton("📜 اليوزرات السابقة", callback_data='history')])
    msg = "اختر نمط اسم المستخدم:" if lang == 'ar' else "Choose username style:"
    query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

def style_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    style_id = query.data.split('_')[1]
    user_data[user_id]['style'] = style_id
    username = generate_username(style_id)
    user_data[user_id]['current_username'] = username

    lang = user_data[user_id]['lang']
    msg = f"اسم المستخدم المقترح:\n\n@{username}\n\nهل تريد التحقق من توافره؟" if lang == 'ar' else f"Suggested username:\n\n@{username}\n\nCheck availability?"
    keyboard = [
        [InlineKeyboardButton("✅ التحقق من التوفر", callback_data='check_available')],
        [InlineKeyboardButton("🔄 توليد جديد", callback_data='generate_new')]
    ]
    query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard))

def check_availability(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    style_id = user_data[user_id]['style']
    lang = user_data[user_id]['lang']

    # محاولة حتى 5 مرات للعثور على اسم متاح
    for _ in range(5):
        username = user_data[user_id]['current_username']
        if random.choice([True, False]):
            user_data[user_id]['used_usernames'].append(username)
            msg = f"🎉 اسم المستخدم @{username} متاح!" if lang == 'ar' else f"🎉 Username @{username} is available!"
            break
        else:
            username = generate_username(style_id)
            user_data[user_id]['current_username'] = username
    else:
        msg = f"❌ لم يتم العثور على اسم متاح." if lang == 'ar' else "❌ Could not find available username."

    keyboard = [
        [InlineKeyboardButton("✅ تحقق مرة أخرى", callback_data='check_available')],
        [InlineKeyboardButton("🔄 توليد جديد", callback_data='generate_new')]
    ]
    query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard))

def generate_new(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    style_id = user_data[user_id]['style']
    username = generate_username(style_id)
    user_data[user_id]['current_username'] = username
    lang = user_data[user_id]['lang']
    msg = f"اسم مستخدم جديد:\n\n@{username}\n\nهل تريد التحقق من توافره؟" if lang == 'ar' else f"New username:\n\n@{username}\n\nCheck availability?"
    keyboard = [
        [InlineKeyboardButton("✅ التحقق من التوفر", callback_data='check_available')],
        [InlineKeyboardButton("🔄 توليد جديد", callback_data='generate_new')]
    ]
    query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard))

def show_history(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    usernames = user_data[user_id].get('used_usernames', [])
    lang = user_data[user_id]['lang']
    if not usernames:
        msg = "❌ لا توجد أسماء مستخدمين محفوظة بعد." if lang == 'ar' else "❌ No usernames saved yet."
    else:
        msg = "📜 الأسماء التي قمت بحجزها:\n\n" if lang == 'ar' else "📜 Your saved usernames:\n\n"
        msg += '\n'.join([f"@{u}" for u in usernames])
    query.edit_message_text(msg)

def main():
    from telegram.ext import ApplicationBuilder

application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(language_button))
application.add_handler(CallbackQueryHandler(style_button))
application.add_handler(CallbackQueryHandler(check_username))
application.add_handler(CallbackQueryHandler(generate_username))
application.add_handler(CallbackQueryHandler(show_history))

application.run_polling()


if __name__ == '__main__':
    main()


