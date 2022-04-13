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
from telethon.tl.types import InputPeerChat
from os.path import exists
from Data import config

PATH = "Sessions/inviter_"


async def join_to_channel(link, sessions, user_id):
    print('joining to channels started')
    working_sessions = []
    for sessionq in sessions:
        print(f"{PATH}/{sessionq}")
        logged = False
        try:
            client = telethon.TelegramClient(f"{PATH}/{sessionq}", config.app_id, config.api_hash)
            #client = telethon.TelegramClient(f"Sessions/new_session.session", config.app_id, config.api_hash)
            await client.connect()
            logged = await client.get_me()
        except Exception as e:
            print(str(e))
            continue
        if (logged):
            print('IS LOGGED')
        else:
            print('NOT LOGGED')
            continue
        await client.start()
        working_sessions.append(sessionq)
        print('before JoinChannel(link)')
        print('after JoinChannel(link)')
        try:
            joinChannel = JoinChannelRequest(link)
            await client(joinChannel)
        except Exception as e:
            print(str(e))
        print('after JoinChannel(link) 2')
        await client.disconnect()
    return working_sessions


async def append_users_to_channel(link, sessions, user_id, usernames, users_count):
    users = []
    invited = 0
    link_ent = ''
    print('append_users_to_channel')
    logged = False
    try:
        print('getting client')
        client = telethon.TelegramClient(f"Sessions/inviter_{user_id}/{sessions[0]}", config.app_id, config.api_hash)
        await client.connect()
        logged = await client.get_me()
    except Exception as e:
        print(str(e))
    print('append_users_to_channel 2')
    
    if (logged):
        print('IS LOGGED 2')
    else:
        print('NOT LOGGED 2')
        return
    await client.start()
    try:
        print('getting LINK_ENT')
        link_ent = await client.get_entity(link)
    except Exception as e:
        print('error LINK_ENT')
        print(str(e))
        return
    for i in usernames:
        u = i.split(';')
        if len(u) < 3:
            continue
        id = u[2].strip()
        if id == "":
            continue
        try:
            print('getting entity')
            print(id)
            obj = await client.get_entity(id)
            users.append(obj)
            print('added')
            print(obj)
        except Exception as e:
            print(str(e))
    await client.disconnect()
    print('append_users_to_channel 3')
    print("working sessions:" + str(len(sessions)))
    for session in sessions:
        try:
            print('getting session')
            print(session)
            client = telethon.TelegramClient(f"Sessions/inviter_{user_id}/{session}", config.app_id, config.api_hash)
            await client.connect()
        except Exception as e:
            print(str(e))
            continue
        await client.start()
        i = 0
        for name in users:
            if i != users_count:
                i = i + 1
                try:
                    print('inviting to channel')
                    print(link_ent)
                    print(name)
                    result = await client(InviteToChannelRequest(link_ent, [name]))
                    invited = invited + 1
                except Exception as e:
                    print(str(e))
                    continue
                print(result)
        await client.disconnect()
    return invited
        
async def start_inviting(user_id, link, users_count, message):
    sessions = []
    for i in os.listdir("Sessions/inviter_" + str(user_id)):
        if i.endswith(".session"):
            sessions.append(i)

    if not exists(f"Sessions/inviter_{str(user_id)}/users.csv"):
        await message.answer(f"нет файла пользователей")
        return 0
    usernames = []
    with open(f"Sessions/inviter_{str(user_id)}/users.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            usernames.append(row[0])
    Helper.logger(f"Sessions: {sessions}")
    Helper.logger(f"Users: {usernames}")
    working_sessions = await join_to_channel(link, sessions, user_id)
    Helper.logger(f"WORKING SESSIONS: {len(working_sessions)}")
    Helper.logger(f"Joined to channels")
    invited = await append_users_to_channel(link, working_sessions, user_id, usernames, users_count)
    await message.answer(f"Процесс завершён\nприглашено: {invited} пользователей\nрабочих сессий: {len(working_sessions)}")
    if invited == 0:
        await message.answer(f"Возможно сессия имеет ограничения попробуйте позже или смените сессию") 
    return invited

    

@dp.message_handler(state = "inviter_1", content_types = ContentType.TEXT)
async def inviter(message: types.Message, state: FSMContext):
    global PATH
    PATH = "Sessions/inviter_"
    PATH = PATH + str(message.from_user.id)
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
    invited = await start_inviting(message.from_user.id, link, users_count, message)








