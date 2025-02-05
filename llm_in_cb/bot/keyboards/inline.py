from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Начать диалог", callback_data='choose_model')],
        [InlineKeyboardButton("Завершить сессию", callback_data='stop')]
    ])


def model_selection():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Llama 3.2", callback_data='model1')],
        [InlineKeyboardButton("Llama 3.2:1b", callback_data='model2')]
    ])
