from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

import os
from loader import dp
import subprocess
from Modules import Helper
import psutil

async def generate_config_file(data: dict, id: str):
    Helper.unzipper(f"Sessions/pervonah_data_{id}/zip{id}.zip", id)
    config_file = f"Sessions/pervonah_data_{id}/config.txt"
    with open(config_file, "w") as file:
        file.write(f"{data['links']}\n{data['comments_file']}\n{data['count']}")
    
print(654)
@dp.message_handler(state = 'pervonah_1', content_types = ContentType.DOCUMENT)
async def pervonah(message: types.Message, state: FSMContext):
    print(123)
    try:
        with open(f"Sessions/pervonah_data_{message.chat.id}/config.txt", "r") as file:
            data = file.read().splitlines()
        print(data[-1])
        p = psutil.Process(int(data[-1]))
        p.kill()
    except:
        print("Oh noo")
    """Download links"""
    path = f"Sessions/pervonah_data_{message.from_user.id}"
    
    try:
        for i in os.listdir(path):
            os.remove(f"{path}/{i}")
        os.rmdir(path)
    except:
        pass
    os.mkdir(f"Sessions/pervonah_data_{message.from_user.id}")
    filename = f"{path}/txt_{message.from_user.id}_links.txt"
    await message.document.download(filename)
    await state.update_data(links = filename.split("/")[-1])
    await message.answer("Укажите кол-во комментарий, одной цифрой.")
    await state.set_state('pervonah_2')


@dp.message_handler(state = 'pervonah_2', content_types = ContentType.TEXT)
async def pervonah(message: types.Message, state: FSMContext):
    """Get counts of comments"""
    await message.answer("Отправьте файл с комментариями в формате .txt")
    await state.update_data(count=message.text)
    await state.set_state('pervonah_3')


@dp.message_handler(state = "pervonah_3", content_types = ContentType.DOCUMENT)
async def pervonah(message: types.Message, state: FSMContext):
    """Download comments file"""
    path = f"Sessions/pervonah_data_{message.from_user.id}"
    filename = f"{path}/txt_{message.from_user.id}_comments.txt"
    await message.document.download(filename)
    await state.update_data(comments_file=filename.split("/")[-1])
    await message.answer("Отправьте файл с сессиями в формате .zip")
    await state.set_state('pervonah_4')


@dp.message_handler(state = "pervonah_4", content_types = ContentType.DOCUMENT)
async def pervonah(message: types.Message, state: FSMContext):
    path = f"Sessions/pervonah_data_{message.from_user.id}"
    filename = f"{path}/zip{message.from_user.id}.zip"
    await message.document.download(filename)
    await state.update_data(sessions_file=filename.split("/")[-1])
    data = await state.get_data()
    links = data['links']
    comments_file = data['comments_file']
    count = data['count']
    sessions_file = filename.split("/")[-1]

    await message.answer(f"<b>Завершено!"
                         f"\nСсылки: <code>{links}</code>"
                         f"\nКомментарии: <code>{comments_file} - {count}</code>"
                         f"\nСессии: <code>{sessions_file}</code></b>"
    )
    await generate_config_file(data, message.from_user.id)
    proj = subprocess.Popen(f"python3 Modules/Pervonah.py {message.from_user.id} {count}",shell=True)
    pid = proj.pid
    config_file = f"Sessions/pervonah_data_{message.from_user.id}/config.txt"
    with open(config_file, "a") as file:
        file.write(f"{pid}")
    