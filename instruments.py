import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from data_base.db_manager import DBManager

loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)
db_manager = DBManager()
