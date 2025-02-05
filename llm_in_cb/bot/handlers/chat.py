from telegram import Update
from telegram.ext import ContextTypes

from llm_in_cb.bot.core.llm import query_llm, get_embeddings, \
    search_vector_database


def validate_input(input_text):
    return bool(input_text and not input_text.isspace())


async def process_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if not validate_input(user_input):
        await update.message.reply_text(
            "Пожалуйста, напиши нормальное сообщение")
        return

    await update.message.reply_text("Обрабатываю запрос...")
    embeddings = get_embeddings(user_input)
    if not isinstance(embeddings, list):
        await update.message.reply_text(
            embeddings.get("error", "Ошибка при получении эмбеддингов."))
        return

    search_results = search_vector_database(embeddings, "default")
    if "error" in search_results:
        await update.message.reply_text(search_results["error"])
        return

    context_from_rag = "\n".join([str(item) for item in
                                  search_results]) if search_results else "Контекст не найден."
    prompt = f"Контекст: {context_from_rag}\n\nВопрос: {user_input}"
    model = context.user_data.get("model", "llama3.2:1b")
    llm_response = query_llm(prompt, model)

    if not llm_response or "Ошибка" in llm_response:
        await update.message.reply_text("Ошибка при обработке запроса модели.")
        return

    await update.message.reply_text(f"Ответ от модели:\n{llm_response}")
