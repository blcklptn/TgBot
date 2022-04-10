from Modules import Helper
import os
import zipfile
import csv

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

import telethon
from loader import dp
import random
from Data import config
PATH = "Sessions/rassilka_"


async def send_to_users(usernames,user_id, sessions, message):
    for user in usernames:
        client = telethon.TelegramClient(f"Sessions/rassilka_{user_id}/{sessions[random.randint(0, len(sessions)-1)]}", config.app_id, config.api_hash)
        await client.start()
        await client.connect()
        await client.send_message(f"@{user[0]}", message)
        await client.disconnect()


@dp.message_handler(state = "rassilka_1", content_types = ContentType.DOCUMENT)
async def rassilka(message: types.Message, state: FSMContext):
    global PATH
    
    PATH += str(message.from_user.id)
    await state.set_state("rassilka_2")
    try:
        for i in os.listdir(PATH):
            os.remove(f"{PATH}/{i}")
        os.rmdir(PATH)
    except:
        pass

    os.mkdir(PATH)
    print("done")
    await message.document.download(f"{PATH}/users.csv")
    await message.answer("Отправьте мне zip архив с сессиями")
    

@dp.message_handler(state = "rassilka_2", content_types = ContentType.DOCUMENT)
async def rassilka(message: types.Message, state: FSMContext):
    await message.document.download(f"{PATH}/sessions.zip")
    await message.answer("Отправьте мне сообщение")
    await state.set_state("rassilka_3")

@dp.message_handler(state = "rassilka_3", content_types = ContentType.TEXT)
async def rassilka(message: types.Message, state: FSMContext):
    global PATH
    messageq = message.text
    usernames = []
    sessions = []
    await message.answer("Начинаю работу!")

    with zipfile.ZipFile(PATH + "/sessions.zip", 'r') as zip_ref:
        zip_ref.extractall(PATH)
    for i in os.listdir(PATH):
        if i.endswith(".session"):
            sessions.append(i)

    with open(PATH + "/users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            usernames.append(row)
    
    await state.finish()
    PATH = "Sessions/rassilka_"
    await send_to_users(usernames, message.from_user.id, sessions, messageq)
