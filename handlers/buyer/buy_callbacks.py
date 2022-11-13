from aiogram.utils.callback_data import CallbackData

buy_project_callback = CallbackData(
    "buy_project_callback", "page", "theme_id", "price_from", "price_up_to"
)
themes_callback = CallbackData(
    "themes_callback", "theme_id", "price_from", "price_up_to"
)
