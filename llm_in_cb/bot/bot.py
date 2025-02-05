from telegram.ext import Application, CommandHandler, CallbackQueryHandler, \
    ConversationHandler, MessageHandler, filters

from llm_in_cb.bot.core.config import TGBOT_API
from llm_in_cb.bot.handlers.chat import process_chat
from llm_in_cb.bot.handlers.model_selection import button, CHOOSING_MODEL, \
    WAITING_FOR_MESSAGE
from llm_in_cb.bot.handlers.start import start, stop


def main():
    app = Application.builder().token(TGBOT_API).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='choose_model')],
        states={
            CHOOSING_MODEL: [
                CallbackQueryHandler(button, pattern='^(model1|model2)$')],
            WAITING_FOR_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_chat)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
