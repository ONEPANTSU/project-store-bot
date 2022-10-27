from aiogram.utils.callback_data import CallbackData

my_projects_callback = CallbackData("my_projects", "page", "is_moderator")
delete_project_callback = CallbackData("delete_project", "id", "page", "is_moderator")
vip_project_callback = CallbackData("vip_project", "id", "page", "is_moderator")
price_changing_callback = CallbackData("price_changing", "id", "page", "is_moderator")
moderators_confirm_callback = CallbackData(
    "moderator_confirm", "project_data_id", "user_id"
)
moderators_reject_callback = CallbackData(
    "moderator_reject", "project_data_id", "user_id"
)
