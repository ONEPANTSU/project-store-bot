project_name = '<b>Название:</b> <a href = "{link}">  {name}</a>'
project_vip = '<b>Объявление:</b> {status}'
project_verified = '<b>Статус:</b> {verified}'
project_themes = '<b>Тематика:</b> {themes}'
project_subs = '<b>Подписчиков:</b> {subs}'
project_income = '<b>Доход в месяц:</b> {income}'
project_comment = '<b>Комментарий:</b> {comm}'
project_seller = '<b>Продавец:</b> @{seller}'
project_price = '<b>Цена:</b> {price}'
project_guarantee = (
    'Гарантируем 100% безопасность при сделках в Telegram.\n'
    '<b>Гарант:</b> {guarantee} "'
)

sell_project_info = (
        project_name + '\n\n' +
        project_vip + '\n' +
        project_themes + '\n' +
        project_subs + '\n' +
        project_income + '\n' +
        project_comment + '\n\n' +
        project_seller + '\n\n' +
        project_price
)

my_project_info = (
        project_name + '\n\n' +
        project_vip + '\n' +
        project_themes + '\n' +
        project_subs + '\n' +
        project_income + '\n' +
        project_comment + '\n\n' +
        project_verified + '\n\n' +
        project_seller + '\n\n' +
        project_price
)

buy_verified_project_info = (
        project_name + '\n\n' +
        project_themes + '\n' +
        project_subs + '\n' +
        project_income + '\n' +
        project_comment + '\n\n' +
        project_verified + '\n\n' +
        project_seller + '\n\n' +
        project_price + '\n\n' +
        project_guarantee
)

buy_not_verified_project_info = (
        project_name + '\n\n' +
        project_themes + '\n' +
        project_subs + '\n' +
        project_income + '\n' +
        project_comment + '\n\n' +
        project_seller + '\n\n' +
        project_price + '\n\n' +
        project_guarantee
)

PROJECT_INFO = {
    "sell": sell_project_info,
    "my": my_project_info,
    "buy_verified": buy_verified_project_info,
    "buy_not_verified": buy_not_verified_project_info
}