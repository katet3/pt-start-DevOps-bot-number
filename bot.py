from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from db_operations import fetch_emails, fetch_phone_numbers, insert_email, insert_phone_number
from text_processing import find_email, find_phone_number
from remote_log_fetcher import get_latest_replication_logs
import logging


import os
from dotenv import load_dotenv
TOKEN = os.getenv('TOKEN')


logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.info("Запуск бота")

INPUT_TEXT, INPUT_CONFIRMATION = range(2)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используй команды для поиска или записи данных.')

def get_repl_logs_command(update, context):
    logs = get_latest_replication_logs()
    update.message.reply_text(logs or "Логи репликации недоступны.")

def get_emails_command(update: Update, context: CallbackContext):
    emails = fetch_emails()
    email_texts = "\n".join([email[0] for email in emails]) if emails else "E-mail адреса не найдены."
    update.message.reply_text(f"Сохранённые e-mail адреса:\n{email_texts}")

def get_phone_numbers_command(update: Update, context: CallbackContext):
    phone_numbers = fetch_phone_numbers()
    phone_number_texts = "\n".join([phone_number[0] for phone_number in phone_numbers]) if phone_numbers else "Номера телефонов не найдены."
    update.message.reply_text(f"Сохранённые номера телефонов:\n{phone_number_texts}")

def find_email_command(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Отправьте мне текст для поиска e-mail адресов.')
    context.user_data['choice'] = 'email'
    return INPUT_TEXT

def find_phone_command(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Отправьте мне текст для поиска телефонных номеров.')
    context.user_data['choice'] = 'phone'
    return INPUT_TEXT

def input_text(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    choice = context.user_data['choice']
    if choice == 'email':
        results = find_email(text)
    else:
        results = find_phone_number(text)
    
    if results:
        reply_text = "\n".join(results)
        update.message.reply_text(f"Найденные {choice}:\n{reply_text}\n\nХотите сохранить их в базу данных? Ответьте 'да' или 'нет'.")
        context.user_data['results'] = results
        return INPUT_CONFIRMATION
    else:
        update.message.reply_text(f"{choice.capitalize()} не найдены.")
        return ConversationHandler.END

def input_confirmation(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() == 'да':
        choice = context.user_data['choice']
        results = context.user_data['results']
        if choice == 'email':
            for email in results:
                insert_email(email)
        elif choice == 'phone':
            for phone_number in results:
                insert_phone_number(phone_number)
        update.message.reply_text("Информация успешно сохранена.")
    else:
        update.message.reply_text("Сохранение отменено.")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Операция отменена.')
    return ConversationHandler.END

def error(update, context):
    logging.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('get_emails', get_emails_command),
                      CommandHandler('get_phone_numbers', get_phone_numbers_command),
                      CommandHandler('find_email', find_email_command),
                      CommandHandler('find_phone_number', find_phone_command)],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text & ~Filters.command, input_text)],
            INPUT_CONFIRMATION: [MessageHandler(Filters.text & ~Filters.command, input_confirmation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('get_repl_logs', get_repl_logs_command))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
