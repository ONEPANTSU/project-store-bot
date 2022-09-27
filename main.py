from aiogram import executor

from instruments import loop, dp

from handlers import main_handlers, buy_handlers, sell_handlers

main_handlers.register_main_handlers(dp=dp)
buy_handlers.register_buy_handlers(dp=dp)
sell_handlers.register_sell_handlers(dp=dp)

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
