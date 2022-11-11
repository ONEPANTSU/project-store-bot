from typing import Any, Dict, Union

from texts.project_info import PROJECT_INFO

start_message = (
    "Здравствуйте, {0.first_name} 🖐! Я тестовый бот для продажи и покупки проектов!"
)

main_menu_massage = "📌 Главное меню 📌"

inform_url = "https://t.me/project_store_guide"
information_message = "Вся информация о боте доступна в телеграм канале:"

sell_menu_message = (
    "✔ Чтобы выставить свой проект на продажу, перейдите в пункт меню «Выставить проект на продажу» "
    "и заполните анкету. Перед появлением на площадке, объявление проходит модерацию. \n\n"
    "✔ Вы можете посмотреть,удалить свои выставленные объявления в пункте меню "
    "«Список моих предложений». Там же вы можете получить или продлить Premium-статус."
)
put_up_for_sale_massage = (
    "🖊Заполните анкету🖊\n\n"
    "Ответьте на пару вопросов, для того чтобы сформировать объяввление. \n\n"
    "⚡ Стоимость размещения объявления: <b> {regular_price} </b> \n"
    "⚡ Стоимость размещения объявления: с Premium-статусом <b> {vip_price} </b> \n"
)
project_name_question = "Напишите название вашего проекта:"
name_so_big_question = (
    "Ваше имя слишком длинное. Напишите название вашего проекта до 50 символов! "
)
link_question = "Оставьте ссылку на ваш проект"
price_question = "Напишите цену вашего проекта"
price_check_question = "Цена должна быть числом. Напишите цену вашего проекта:"
subscribers_question = "Сколько подписчиков у вашего проекта?"
subscribers_check_question = "Укажите количество подписчиков числом. Напишите сколько подписчиков у вашего проекта:"
to_many_subscribers_question = (
    "Введено слишком большое число! Сколько подписчиков у вашего проекта?"
)
income_question = "Какой доход у вашего проекта?"
income_check_question = "Укажите доход проекта числом. Какой доход у вашего проекта:"
themes_question = "Выберите не более 3-х тематик вашего проекта:"
themes_warn_question = "Такой темы нет в списке! Выберите тему из списка"
themes_warn_2_question = "Данная тема уже добавлена!"
themes_plus_1_question = "Выберите ещё одну тему"
themes_plus_question = "Хотите выбрать ещё тему?"
yes_question = "Да"
no_question = "Нет"
yes_or_no_question = "Ответ должен быть 'Да' или 'Нет' "
comment_question = "Добавьте комментарий к обьявлению:"
comment_so_big_question = (
    "Комментарий слишком длинный! Напишите комментарий не превышая 1000 символов!"
)
status_question = (
    "Хотите ли получить 💎 Premium-статус 💎? \n\n"
    "Для лучшего продвижения продажи своих проектов вы можете получить Premium-статус, "
    "он действителен 7 дней. \n"
    "Вы получаете:\n"
    "  🌟 Ваш проект находится в топах списка у покупателей; \n"
    "  🌟 Быстрая модерация; \n"
    "  🌟 Возможность редактирования цены проекта; \n\n"
    "Стоимость Premium-статуса на неделю:  ⚡ <b> {vip_price}₽ </b> ⚡"
)
status_yes_question = "Ура, теперь вы счталивый обладатель 👑 Premium-статуса 👑!!!"
confirm_question = (
    "Данные введены верно? Если да, то перейдите к оплате. "
    "При нажатии кнопки 'Отмена' Вы вернётесь в главное меню.\n\n"
    + PROJECT_INFO["sell"]
)
payment_message = "Начинается процесс оплаты ⏳"

cancellation_question = "Отмена"
save_project_question = "🎉 Ваше обьявление сохранено! 🎉"

get_list_of_projects_message = "🗄 Выставленные на продажу предложения 🗄"

buy_menu_message = (
    "✔ Здесь можно посмотреть список проектов на бирже \n\n"
    "✔ Воспользовавшись параметрами поиска, вы можете отсортировать все проекты"
    " по цене и тематикам."
)
chose_themes_message = "Выберите интересные тематики"
question_theme_message = "Хотите выбрать тематику?"
themes_list_message = "Список тематик"
themes_list_smile_message = "📋"
question_price_message = "Хотите выбрать цену?"
chose_price_from_message = "Введите цену от: "
chose_price_up_to_message = "Введите цену до: "
show_all_projects_message = "Показать все предложения"
all_projects_message = "Все предложения"
not_recognized_message = "Сообщение не распознано☹. Попробуйте еще раз!"
error_not_digit_price_from_message = (
    "Ответ должен быть положительным числом! Введите цену от: "
)
error_not_digit_price_upto_message = (
    "Ответ должен быть положительным числом! Введите цену до: "
)
error_upto_bigger_then_from_message = (
    "Цена 'до' должна быть больше цены 'от'. Введите цену до: "
)
list_is_empty_message = "Проектов по вашему запросу не найдено"


vip_payment_label = "Установить Premium cтатус проекту!"
sell_payment_label = "Разместить объявление!"
sell_payment_title = "Оплата"
sell_payment_description = "Оплата за размещение объявления"
vip_payment_description = "Оплата Premium-статуса"
successful_payment_message = "Оплата произведена успешно!"

show_my_project_message = PROJECT_INFO["my"]
show_verified_project_message = PROJECT_INFO["buy_verified"]
show_not_verified_project_message = PROJECT_INFO["buy_not_verified"]
deleted_project_message = "Объявление удалено! 📍"
not_deleted_project_message = "Объявление не удалено 🛑"
confirm_deleting_message = "Вы действительно хотите удалить объявление?"
empty_projects_message = "У вас не выставлено ни одного объявления.🤔"
projects_none_message = "Проектов не найдено"

command_error_message = "Сообщение не распознано ☹"

moderation_message = "Ожидайте. Ваша заявка на модерации!"
moderator_confirm_message = (
    "Новая заявка на размещение объявления ждёт подтверждения!\n\n"
    + PROJECT_INFO["sell"]
)
rejected_project_message = "К сожалению, ваш проект '%s' не прошёл модерацию! ☹"
empty_username_message = "У вас не задано имя пользователя в телеграме! Измените настройки и возвращайтесь! 😊"
already_in_moderation_message = "Ваш проект находится на модерации! Ожидайте ответа!"

change_price_message = price_question
price_changing_success_message = "Цена проекта успешно изменена!"
price_changing_confirm_message = "Вы уверены, что хотите изменить цену?"

vip_project = "Premium 👑"
regular_project = "Обычное 🗿"
free_payment_message = "Бесплатно!"

verified = "Проверено ✅"
not_verified = "Идёт проверка..."

need_promo_code_message = "Ваш проект прошёл проверку! Воспользоваться промокодом?"
input_promo_code_message = "Введите промокод:"
wrong_promo_code_message = "Неверный промокод! Попробовать ещё раз?"

vip_need_promo_code_message = "Воспользоваться промокодом?"

settings_message = "🛠️ Настройки бота 🛠️"
moderators_message = "Модераторы:"
change_guarantee_message = "Введите новое имя гаранта"
confirm_change_guarantee_message = "Имя гаранта введено верно?"
id_add_moderator_message = "Введите id нового модератора"
name_add_moderator_message = "Введите ник нового модератора"
id_check_message = "ID должен быть числом! Введите id нового модератора"
confirm_add_moderator_message = "Имя модератора и id введено верно?"
update_save_message = "Обновления сохранены!"

MESSAGES = {
    "start": start_message,
    "inform_url": inform_url,
    "information": information_message,
    "sell_menu": sell_menu_message,
    "put_up_for_sale": put_up_for_sale_massage,
    "project_name": project_name_question,
    "name_so_big": name_so_big_question,
    "link": link_question,
    "price": price_question,
    "price_check": price_check_question,
    "subscribers": subscribers_question,
    "subscribers_check": subscribers_check_question,
    "to_many_subscribers": to_many_subscribers_question,
    "themes": themes_question,
    "themes_warn": themes_warn_question,
    "themes_warn_2": themes_warn_2_question,
    "themes_plus_1": themes_plus_1_question,
    "themes_plus": themes_plus_question,
    "yes": yes_question,
    "no": no_question,
    "yes_or_no": yes_or_no_question,
    "income": income_question,
    "income_check": income_check_question,
    "comment": comment_question,
    "comment_so_big": comment_so_big_question,
    "status": status_question,
    "status_yes": status_yes_question,
    "confirm": confirm_question,
    "cancellation": cancellation_question,
    "save_project": save_project_question,
    "get_list_of_projects": get_list_of_projects_message,
    "main_menu": main_menu_massage,
    "buy_menu": buy_menu_message,
    "chose_themes": chose_themes_message,
    "chose_price_from": chose_price_from_message,
    "chose_price_up_to": chose_price_up_to_message,
    "vip_payment": vip_payment_label,
    "sell_payment": sell_payment_label,
    "sell_payment_title": sell_payment_title,
    "sell_payment_description": sell_payment_description,
    "vip_payment_description": vip_payment_description,
    "successful_payment": successful_payment_message,
    "show_my_project": show_my_project_message,
    "show_verified_project": show_verified_project_message,
    "show_not_verified_project": show_not_verified_project_message,
    "deleted_project": deleted_project_message,
    "not_deleted_project": not_deleted_project_message,
    "confirm_deleting": confirm_deleting_message,
    "empty_projects": empty_projects_message,
    "project_none": projects_none_message,
    "command_error": command_error_message,
    "error_not_digit_price_from": error_not_digit_price_from_message,
    "error_not_digit_price_upto": error_not_digit_price_upto_message,
    "error_upto_bigger_then_from": error_upto_bigger_then_from_message,
    "question_theme": question_theme_message,
    "question_price": question_price_message,
    "show_all_projects": show_all_projects_message,
    "all_projects": all_projects_message,
    "not_recognized": not_recognized_message,
    "list_is_empty": list_is_empty_message,
    "themes_list": themes_list_message,
    "themes_list_smile": themes_list_smile_message,
    "moderation": moderation_message,
    "moderator_confirm": moderator_confirm_message,
    "rejected_project": rejected_project_message,
    "empty_username": empty_username_message,
    "already_in_moderation": already_in_moderation_message,
    "vip_project": vip_project,
    "regular_project": regular_project,
    "verified": verified,
    "not_verified": not_verified,
    "change_price": change_price_message,
    "price_changing_success": price_changing_success_message,
    "price_changing_confirm": price_changing_confirm_message,
    "need_promo_code": need_promo_code_message,
    "input_promo_code": input_promo_code_message,
    "wrong_promo_code": wrong_promo_code_message,
    "vip_need_promo_code": vip_need_promo_code_message,
    "free_payment": free_payment_message,
    "settings": settings_message,
    "moderators": moderators_message,
    "change_guarantee": change_guarantee_message,
    "confirm_change_guarantee": confirm_change_guarantee_message,
    "id_add_moderator": id_add_moderator_message,
    "name_add_moderator": name_add_moderator_message,
    "id_check": id_check_message,
    "confirm_add_moderator": confirm_add_moderator_message,
    "update_save": update_save_message,
}
