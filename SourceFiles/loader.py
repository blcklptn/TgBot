from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
import json
from Modules import Helper
from Data import config

""" Get bot name with telegram api """
bot_name = requests.get(f"https://api.telegram.org/bot{config.BotToken}/getMe").text
data = json.loads(bot_name)
bot_name = data.get('result').get('username')

Helper.logger(f"Bot name: @{bot_name}", "INFO")


""" Initialize bot """
bot = Bot(token= config.BotToken , parse_mode=types.ParseMode.HTML) 
storage = MemoryStorage()  # For storing FSM data
dp = Dispatcher(bot, storage=storage)  # For handling messages

Helper.logger(f"Bot started", "INFO")