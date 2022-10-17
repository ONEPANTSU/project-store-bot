from aiogram import executor

from useful.instruments import dp, loop
from useful.registrator import register_handlers
from useful.schedule import start_timer_process

register_handlers(dp=dp)

if __name__ == "__main__":
    start_timer_process()
    executor.start_polling(dp, loop=loop)
