from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES


async def information_handler(message: Message):
    await help_inform(message)


async def help_command(message: Message):
    await help_inform(message)


async def help_inform(message: Message):
    await message.answer(text=MESSAGES["information"], reply_markup=inform_keyboard())


def inform_keyboard():
    inform_button = InlineKeyboardButton(
        text=BUTTONS["information"], url=MESSAGES["inform_url"]
    )
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(inform_button)
    return keyboard



def register_information_handlers(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=[COMMANDS["help"]])
    dp.register_message_handler(information_handler, text=BUTTONS["information"])
