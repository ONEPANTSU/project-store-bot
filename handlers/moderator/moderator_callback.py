from aiogram.utils.callback_data import CallbackData

delete_moderator_callback = CallbackData("delete_moderator", "id", "page")
moderator_page_callback = CallbackData("moderator_page", "page")
chose_moderator_callback = CallbackData("chose_moderator", "id", "page")
delete_promo_callback = CallbackData("delete_promo", "code")
add_promo_callback = CallbackData("add_promo")
