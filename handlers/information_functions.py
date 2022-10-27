from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from texts.buttons import BUTTONS
from texts.messages import MESSAGES


async def help_inform(message: Message):
    await message.answer(text=MESSAGES["information"], reply_markup=inform_keyboard())


def inform_keyboard():
    inform_button = InlineKeyboardButton(
        text=BUTTONS["information"], url=MESSAGES["inform_url"]
    )
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(inform_button)
    return keyboard
