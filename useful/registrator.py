from aiogram import Dispatcher

from handlers.buyer import buy_handlers
from handlers.information import information_handlers
from handlers.main import main_handlers
from handlers.moderator import moderator_handlers
from handlers.seller.handlers import my_projects_handlers, sell_handlers


def register_handlers(dp: Dispatcher):
    main_handlers.register_main_handlers(dp=dp)
    buy_handlers.register_buy_handlers(dp=dp)
    sell_handlers.register_sell_handlers(dp=dp)
    my_projects_handlers.register_my_projects_handlers(dp=dp)
    moderator_handlers.register_moderator_handlers(dp=dp)
    information_handlers.register_information_handlers(dp=dp)
