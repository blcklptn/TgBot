from aiogram import types

def MainKeyboard() -> types.reply_keyboard.ReplyKeyboardMarkup:
    """Return keyboard with main buttons"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True) 
    keyboard.add(*["😏Инвайт", "😡Жалобы"])
    keyboard.add(*["😼Просмотры", "👺Первонахер"])
    keyboard.add(*["👨‍💻Рассылка сообщений", "🧔🏿Вступление/выход из группы и чата"])
    keyboard.add(*["🗣Голосовые опросы", "👍Реакции"])
    keyboard.add(*["👾Проверка номеров", "🧩Прокси", "📲Смена Api Hash"])
    return keyboard
