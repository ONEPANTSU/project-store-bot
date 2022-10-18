from aiogram.utils.callback_data import CallbackData

my_projects_callback = CallbackData("my_projects", "page", "is_moderator")
delete_project_callback = CallbackData("delete_project", "id", "page", "is_moderator")
