from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from llm_in_cb.bot.keyboards.inline import model_selection

CHOOSING_MODEL, WAITING_FOR_MESSAGE = range(2)


async def choose_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Выберите модель",
                                                   reply_markup=model_selection())
    return CHOOSING_MODEL


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'choose_model':
        return await choose_model(update, context)
    elif query.data == 'stop':
        await query.message.reply_text("Сессия завершена.")
        return ConversationHandler.END
    elif query.data in ['model1', 'model2']:
        model_map = {'model1': "llama3.2", 'model2': "llama3.2:1b"}
        context.user_data['model'] = model_map[query.data]
        await query.message.reply_text(
            f"Выбрана модель {model_map[query.data]}. Отправьте сообщение.")
        return WAITING_FOR_MESSAGE