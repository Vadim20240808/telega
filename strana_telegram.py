import telegram
from tqdm.contrib import telegram

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from collections import defaultdict

# Сопоставление language_code со странами (пример)
LANGUAGE_TO_COUNTRY = {
    'ru': 'Россия 🇷🇺',
    'en': 'США/Великобритания 🇺🇸🇬🇧',
    'de': 'Германия 🇩🇪',
    'fr': 'Франция 🇫🇷',
    'es': 'Испания 🇪🇸',
    'it': 'Италия 🇮🇹',
    'tr': 'Турция 🇹🇷',
    'ar': 'Арабские страны 🇸🇦',
    'ja': 'Япония 🇯🇵',
    'zh': 'Китай 🇨🇳',
}

def get_country_command(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type not in ('group', 'supergroup', 'channel'):
        update.message.reply_text("Эта команда работает только в группах и каналах!")
        return

    try:
        admins = context.bot.get_chat_administrators(chat.id)
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
        return

    lang_counts = defaultdict(int)
    for admin in admins:
        user = admin.user
        if user.language_code:
            lang_code = user.language_code.split('-')[0].lower()
            lang_counts[lang_code] += 1

    if lang_counts:
        most_common = max(lang_counts.items(), key=lambda x: x[1])
        country = LANGUAGE_TO_COUNTRY.get(most_common[0], 'Неизвестная страна')
        update.message.reply_text(
            f"Предполагаемая страна чата: {country}\n"
            f"На основе языка администраторов: {most_common[0]} ({most_common[1]} чел.)"
        )
    else:
        update.message.reply_text("Не удалось определить язык администраторов")

def main():
    TOKEN = "ВАШ_ТОКЕН_БОТА"
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("country", get_country_command))

    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()