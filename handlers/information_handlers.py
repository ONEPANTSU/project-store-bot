from aiogram import Dispatcher
from aiogram.types import Message

from handlers.information_functions import help_inform
from texts.buttons import BUTTONS
from texts.commands import COMMANDS


async def information_handler(message: Message):
    await help_inform(message)


async def help_command(message: Message):
    await help_inform(message)


def register_information_handlers(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=[COMMANDS["help"]])
    dp.register_message_handler(information_handler, text=BUTTONS["information"])
