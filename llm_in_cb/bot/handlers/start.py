from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from llm_in_cb.bot.keyboards.inline import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я бот, чем могу помочь?",
                                    reply_markup=main_menu())


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Сессия завершена.")
    return ConversationHandler.END
