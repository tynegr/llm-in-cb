import json
import queue
import threading

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, filters, MessageHandler, CommandHandler, \
    ContextTypes, ConversationHandler, CallbackQueryHandler

from llm_in_cb.config import CONFIG_PATH, VECTOR_DB_API_URL, EMBEDDING_API_URL

process_lock = threading.Lock()

task_queue = queue.Queue()


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config(CONFIG_PATH)

TGBOT_API = config["telegram_bot"]["token"]


def get_embeddings(text):
    try:
        response = requests.post(f"{EMBEDDING_API_URL}/embed",
                                 json={"text": text})
        response.raise_for_status()
        return response.json().get("embeddings")
    except Exception as e:
        return {"error": f"Error getting embeddings: {str(e)}"}


def search_vector_database(embeddings, category):
    try:
        response = requests.post(f"{VECTOR_DB_API_URL}/search", json={
            "embeddings": embeddings,
            "category": category
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Error searching database: {str(e)}"}


async def process_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if not validate_input(user_input):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Пж напиши нормальное сообщение")
        return

    await update.message.reply_text("Обрабатываю запрос...")

    embeddings = get_embeddings(user_input)
    if "error" in embeddings:
        await update.message.reply_text(embeddings["error"])
        return

    category = "default"
    search_results = search_vector_database(embeddings, category)
    if "error" in search_results:
        await update.message.reply_text(search_results["error"])
        return

    if search_results:
        response_text = "\n\n".join(
            [f"Контент: {item}" for item in search_results])
    else:
        response_text = "Ничего похожего не найдено."

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response_text)


def validate_input(input):
    return bool(input and not input.isspace())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать диалог", callback_data='choose_model')],
        [InlineKeyboardButton("Завершить сессию", callback_data='stop')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Я ботик, че хотел?",
                                    reply_markup=reply_markup)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Сессия завершена. Бот больше не будет принимать сообщения.")
    return ConversationHandler.END


async def choose_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("model1", callback_data='model1')],
        [InlineKeyboardButton("model2", callback_data='model2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Выберите модель",
                                   reply_markup=reply_markup)

    return CHOOSING_MODEL


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'choose_model':
        await choose_model(update, context)
        return CHOOSING_MODEL
    elif query.data == 'stop':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Сессия завершена. Бот больше не будет принимать сообщения.")
        return ConversationHandler.END
    elif query.data in ['model1', 'model2']:
        context.user_data['model_name'] = query.data
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Выбрана модель {query.data}. Теперь отправьте сообщение.")
        return WAITING_FOR_MESSAGE


WAITING_FOR_MESSAGE, CHOOSING_MODEL = range(2)


def main():
    app = Application.builder().token(TGBOT_API).build()
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('choose_model', choose_model),
            CallbackQueryHandler(button, pattern='^choose_model$'),
        ],
        states={
            CHOOSING_MODEL: [
                CallbackQueryHandler(button, pattern='^model1$'),
                CallbackQueryHandler(button, pattern='^model2$')
            ],
            WAITING_FOR_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_chat)
            ],
        },
        fallbacks=[
            CommandHandler('stop', stop),
            CallbackQueryHandler(button, pattern='^stop$')
        ]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conversation_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
