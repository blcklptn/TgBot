from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from loader import dp
import os
from Modules import Helper
import zipfile
import csv
import telethon
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel ,InputUser
from telethon.tl.functions.contacts import ResolveUsernameRequest

from Data import config

PATH = "Sessions/inviter_"


async def join_to_channel(link, sessions, user_id):
    for sessionq in sessions:
        client = telethon.TelegramClient(f"Sessions/inviter_{user_id}/{sessionq}", config.app_id, config.api_hash)
        await client.start()
        await client.connect()
        await client(JoinChannelRequest(link))
        await client.disconnect()


async def append_users_to_channel(link, sessions, user_id, usernames, users_count):
    users = []
    client = telethon.TelegramClient(f"Sessions/inviter_{user_id}/{sessions[0]}", config.app_id, config.api_hash)
    await client.start()
    await client.connect()
    for i in usernames:
        users.append(await client.get_entity(i))
    link_ent = await client.get_entity(link)
    await client.disconnect()
    
    for session in sessions:
         client = telethon.TelegramClient(f"Sessions/inviter_{user_id}/{session}", config.app_id, config.api_hash)
         await client.start()
         await client.connect()
         i = 0
         for name in users:
            if i != users_count:
                i = i + 1
                print(name)
                result = await client(InviteToChannelRequest(link_ent, [name]))
                print(result)
         await client.disconnect()
            
        
async def start_inviting(user_id, link, users_count):
    sessions = []
    for i in os.listdir("Sessions/inviter_" + str(user_id)):
        if i.endswith(".session"):
            sessions.append(i)

    usernames = []
    with open(f"Sessions/inviter_{str(user_id)}/users.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            usernames.append(row[0])
    Helper.logger(f"Sessions: {sessions}")
    Helper.logger(f"Users: {usernames}")
    await join_to_channel(link, sessions, user_id)
    Helper.logger(f"Joined to channels")
    await append_users_to_channel(link, sessions, user_id, usernames, users_count)

    

@dp.message_handler(state = "inviter_1", content_types = ContentType.TEXT)
async def inviter(message: types.Message, state: FSMContext):
    global PATH
    PATH += str(message.from_user.id)
    try:
        for i in os.listdir(PATH):
            os.remove(f"{PATH}/{i}")
        os.rmdir(PATH)
    except:
        pass
    os.mkdir(PATH)
    print("done")
    link = message.text
    await state.update_data(link = link)
    await state.set_state('inviter_2')
    await message.answer("Отправьте файл с пользователями в формате .csv")

@dp.message_handler(state = "inviter_2", content_types = ContentType.DOCUMENT)
async def inviter(message: types.Message, state: FSMContext):
    print("state2")
    await message.document.download(f"{PATH}/users.csv")
    await state.set_state("inviter_3")
    await message.answer("Отправьте файл с сессиями в формате .zip")
    

@dp.message_handler(state = "inviter_3", content_types = ContentType.DOCUMENT)
async def inviter(message: types.Message, state: FSMContext):
    print("state3")
    await message.document.download(f"{PATH}/sessions.zip")
    await state.update_data(sessions_file = "sessions.zip")
    await message.answer("Сколько пользователей вы хотите приглашать с помощью одной сессии?")
    await state.set_state("inviter_4")

@dp.message_handler(state = "inviter_4", content_types = ContentType.TEXT)
async def inviter(message: types.Message, state: FSMContext):
    await state.update_data(users_count = message.text)
    await message.answer("Начинаю работу...")

    data = await state.get_data()
    link = data['link']
    csv_file = "users.csv"
    sessions_file = data['sessions_file']
    users_count = data['users_count']

    with zipfile.ZipFile(PATH + "/sessions.zip", 'r') as zip_ref:
        zip_ref.extractall(f"Sessions/inviter_{message.from_user.id}/")

    await message.answer(f"<b>Ссылка: <code>{link}</code>\nФайл сессий: <code>{sessions_file}</code>\nПользователя за сессию: <code>{users_count}</code>\n</b>")
    await state.finish()
    await start_inviting(message.from_user.id, link, users_count)








