from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from Keyboards import MainKeyboard
import logging

from Modules import pervonaxer, inviter, rassilka


@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=MainKeyboard.MainKeyboard())

@dp.message_handler(commands=['help'], state='*')
async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer(f"Список команд:\n /start - Начать диалог\n /help - Помощь")

@dp.message_handler(text = '😏Инвайт', state='*')
async def waiting(message: types.Message, state: FSMContext):
    await state.set_state('inviter_1')
    await message.answer("Отправьте ссылку на канал/группу")
    

@dp.message_handler(text = '😡Жалобы', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(text = '😼Просмотры', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(text = '👺Первонахер', state='*')
async def waiting(message: types.Message, state: FSMContext):
    await state.set_state('pervonah_1')
    await message.answer('<b>Отправьте ссылку на группу на 👺Первонахер👺 в формате .txt</b>\n\n'
                         'Примеры:\n'
                         'https://t.me/chatname\n')
                
@dp.message_handler(text = '👨‍💻Рассылка сообщений', state='*')
async def waiting(message: types.Message, state: FSMContext):
    await state.set_state("rassilka_1")
    await message.answer("Отправьте .csv с юзернейнами")

@dp.message_handler(text = '🧔🏿Вступление/выход из группы и чата', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(text = '🗣Голосовые опросы', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(text = '👍Реакции', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(text = '👾Проверка номеров', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass

@dp.message_handler(text = '🧩Прокси', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(text = '📲Смена Api Hash', state='*')
async def waiting(message: types.Message, state: FSMContext):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)