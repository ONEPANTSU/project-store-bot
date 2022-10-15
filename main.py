from aiogram import executor

from handlers import main_handlers
from handlers.buyer import buy_handlers
from handlers.seller import my_projects_handlers, sell_handlers
from instruments import dp, loop

main_handlers.register_main_handlers(dp=dp)
buy_handlers.register_buy_handlers(dp=dp)
sell_handlers.register_sell_handlers(dp=dp)
my_projects_handlers.register_my_projects_handlers(dp=dp)

if __name__ == "__main__":
    executor.start_polling(dp, loop=loop)
