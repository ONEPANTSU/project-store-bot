from aiogram.types import ReplyKeyboardRemove

from handlers.buyer.buy_functions import show_all_projects
from handlers.information.information_functions import help_inform
from handlers.main.main_functions import main_menu
from handlers.seller.handlers.my_projects_functions import my_project_index_handler
from handlers.seller.inner_functions.sell_functions import put_up_for_sale
from texts.commands import COMMANDS
from texts.messages import MESSAGES


async def commands_handler(message):
    answer = message.text.lstrip("/")
    if answer == COMMANDS["start"]:
        await main_menu(
            message,
            message_text=MESSAGES["start"].format(
                message.from_user, reply_markup=ReplyKeyboardRemove()
            ),
        )
    elif answer == COMMANDS["help"]:
        await help_inform(message)
    elif answer == COMMANDS["new_project"]:
        await put_up_for_sale(message)
    elif answer == COMMANDS["my_projects"]:
        await my_project_index_handler(message)
    elif answer == COMMANDS["search_project"]:
        await show_all_projects(message)
    elif answer == COMMANDS["back"]:
        await main_menu(message, message_text=MESSAGES["main_menu"])
