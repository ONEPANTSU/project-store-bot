from aiogram.utils.callback_data import CallbackData

buy_project_callback = CallbackData(
    "buy_project_callback", "page", "theme_id", "price_from", "price_up_to", "status"
)
themes_callback = CallbackData(
    "themes_callback", "theme_id", "price_from", "price_up_to"
)
chose_search_params_callback = CallbackData(
    "chose_params_callback", "page", "theme_id", "price_from", "price_up_to"
)
search_by_price_params_callback = CallbackData(
    "price_params_callback", "theme_id"
)
search_by_theme_params_callback = CallbackData(
    "theme_params_callback", "price_from", "price_up_to"
)