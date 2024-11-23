import requests
import json
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackQueryHandler
import threading
import queue
import asyncio

process_lock = threading.Lock()

task_queue = queue.Queue()

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)

config = load_config('ips_rag_llm_tg_bot\config_api.json')

TGBOT_API = config["telegram_bot"]["token"]
RAG_API_KEY = config["rag_api"]["token"]
LLM_API_KEY = config["llm_api"]["token"]

def query_rag(user_input):
    # headers = {"Authorization": f"Bearer {RAG_API_KEY}"}
    # payload = {"query": user_input}
    # response = requests.post(RAG_API_URL, json=payload, headers=headers)
    
    # if response.status_code == 200:
    #     return response.json()  # Предполагаем, что результат — JSON
    # else:
    #     return {"error": f"RAG API Error: {response.status_code}"}
    return 'ещкере'


def query_llm(prompt, model_name):
    # LLM_API_KEY = config[model_name]["token"]
    # openai.api_key = LLM_API_KEY

    # response = openai.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "Ты большой эксперт и знаток русского нижнего интернета"},
    #         {"role": "user", "content": prompt}
    #     ],
    #     temperature=0.7,
    #     max_tokens=150
    # )
    
    # return response["choices"][0]["message"]["content"]
    return 'аххахахахха'

def validate_input(input):
    if input == "":
        return False
    if input.isspace():
        return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать диалог", callback_data='choose_model')],
        [InlineKeyboardButton("Завершить сессию", callback_data='stop')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем приветственное сообщение с клавиатурой
    await update.message.reply_text("Я ботик, че хотел?", reply_markup=reply_markup)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сессия завершена. Бот больше не будет принимать сообщения.")
    return ConversationHandler.END

async def choose_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("model1", callback_data='model1')],
        [InlineKeyboardButton("model2", callback_data='model2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите модель", reply_markup=reply_markup)

    return CHOOSING_MODEL


async def process_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if not validate_input(update.message.text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пж напиши нормальное сообщение")
        return
    await update.message.reply_text("Обрабатываю запрос...")

    model_name = context.user_data.get('model_name', 'model1')  # Если модель не выбрана, используем 'default_model'
    # rag_response = query_rag(user_input)
    # if "error" in rag_response:
    #     await update.message.reply_text(rag_response["error"])
    #     return

    context_from_rag = 'жопа' # rag_response.get("context", "Контекст отсутствует.")
    prompt = f"На основе следующего контекста: {context_from_rag}, ответь на вопрос: {user_input}"

    llm_response = query_llm(prompt, model_name) if model_name == 'model1' else 'hahahahahhaha'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=llm_response)
    return WAITING_FOR_MESSAGE


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'choose_model':
        await choose_model(update, context)
        return CHOOSING_MODEL
    elif query.data == 'stop':
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Сессия завершена. Бот больше не будет принимать сообщения.")
        return ConversationHandler.END
    elif query.data in ['model1', 'model2']:
        context.user_data['model_name'] = query.data
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Выбрана модель {query.data}. Теперь отправьте сообщение.")
        return WAITING_FOR_MESSAGE


WAITING_FOR_MESSAGE, CHOOSING_MODEL = range(2)

def main():
    app = Application.builder().token(TGBOT_API).build()
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('choose_model', choose_model),
            CallbackQueryHandler(button, pattern='^choose_model$'),
        ],  # Входной обработчик для команды /start
        states={
            CHOOSING_MODEL: [
                CallbackQueryHandler(button, pattern='^model1$'),
                CallbackQueryHandler(button, pattern='^model2$')
            ],
            WAITING_FOR_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_chat)
            ],
        },
        fallbacks = [
            CommandHandler('stop', stop),
            CallbackQueryHandler(button, pattern='^stop$')
        ]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conversation_handler)

    app.run_polling()

if __name__ == "__main__":
    main()