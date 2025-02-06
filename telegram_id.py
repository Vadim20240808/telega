from tqdm.contrib import telegram
import python-telegram-bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашего бота (получите у @BotFather)
TOKEN = "ВАШ_ТОКЕН_БОТА"


def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    update.message.reply_text(
        "Привет! Отправь любое сообщение, и я покажу твой ID и ID этого чата."
    )


def show_ids(update: Update, context: CallbackContext):
    """Показывает ID пользователя и чата"""
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    response = (
        f"🆔 Ваш ID пользователя: `{user_id}`\n"
        f"💬 ID этого чата: `{chat_id}`"
    )

    update.message.reply_text(response, parse_mode="Markdown")


def main():
    # Создаем объект Updater и передаем токен
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик для любых текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, show_ids))

    # Запускаем бота
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()