import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я Федор, помогу тебе создать Telegram-бота. Опиши свое техническое задание.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Создай Telegram-бота для задачи: {user_input}",
        max_tokens=500
    )
    generated_code = response.choices[0].text.strip()

    bot_name = "generated_bot.py"
    with open(bot_name, "w") as bot_file:
        bot_file.write(generated_code)

    deploy_bot(update, bot_name)

def deploy_bot(update: Update, bot_name: str) -> None:
    try:
        os.system(f"python3 {bot_name} --check")

        target_directory = "/path/to/bots"
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        os.rename(bot_name, os.path.join(target_directory, bot_name))

        os.system(f"docker build -t {bot_name} . && docker run -d --name {bot_name} {bot_name}")

        update.message.reply_text(f"Бот успешно создан и задеплоен. Название файла: {bot_name}")
    except Exception as e:
        update.message.reply_text(f"Ошибка при деплое бота: {e}")

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()