from data_base.project import Project
from useful.instruments import db_manager


def get_projects_list_by_theme_id(theme_id):
    """
    This function creates SELECT query for getting all Project class's objects by theme's id.

    :param theme_id: id of the theme
    :type theme_id: :obj: `int`

    :return: list of the Project class's objects with the concrete theme
    :rtype: :list::class:`data_base.project.Project`
    """
    return to_parse_project_list(db_manager.get_projects_info_by_theme_id(theme_id))


def get_projects_list_by_themes_id(themes_id):
    """
    This function creates SELECT query for getting all Project class's objects by themes's id.

    :param themes_id: list with id of the themes
    :type themes_id: :list: `int`

    :return: list of the Project class's objects with the concrete theme
    :rtype: :list::class:`data_base.project.Project`
    """
    return remove_duplicates(get_project_list_with_duplicates(themes_id))


def remove_duplicates(projects_list):
    id_list = list()
    for element in projects_list:
        if element.id in id_list:
            projects_list.remove(element)
        else:
            id_list.append(element.id)
    return projects_list


def get_project_list_with_duplicates(themes_id):
    projects_list = list()
    for theme_id in themes_id:
        projects_list = projects_list + get_projects_list_by_theme_id(theme_id)
    return projects_list


def get_projects_list_by_seller_name(seller_name):
    """
    This function creates SELECT query for getting all Project class's objects by seller's name.

    :param seller_name: telegram name of the seller
    :type seller_name: :list: `str`

    :return: list of the Project class's objects with the concrete theme
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_info = db_manager.get_projects_info_by_seller_name(seller_name)
    return get_parsed_project_list(projects_info)


def get_moderator_all_project_list():
    """
    This function creates SELECT query for getting all Project class's objects.

    :return: list of the Project class's objects
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_id = db_manager.get_moderator_all_projects_id()
    projects_info = create_all_projects_info(projects_id)
    return get_parsed_project_list(projects_info)


def get_all_project_list():
    """
    This function creates SELECT query for getting all Project class's objects.

    :return: list of the Project class's objects
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_id = db_manager.get_all_projects_id()
    projects_info = create_all_projects_info(projects_id)
    return get_parsed_project_list(projects_info)


def get_parsed_project_list(projects_info):
    projects_list = list()
    if len(projects_info) != 0:
        projects_list = to_parse_project_list(projects_info)
    return projects_list


def create_all_projects_info(projects_id):
    projects_info = list()
    for project_id in projects_id:
        projects_info.append(db_manager.get_all_project_info_by_id(project_id))
    return projects_info


def get_vip_project_list():
    """
    This function creates SELECT query for getting VIP Project class's objects.

    :return: list of the Project class's objects with VIP status
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_id = db_manager.get_vip_projects_id()
    projects_info = create_all_projects_info(projects_id)
    return get_parsed_project_list(projects_info)


def get_project_list_by_filter(theme_id="None", price_from="None", price_up_to="None"):
    """
    This function creates SELECT query for getting all Project class's objects by filter.

    :param theme_id: id of the themes
    :type theme_id: :obj: `int`
    :param price_from: start of price's diapason
    :type price_from: :obj: `int`
    :param price_up_to:end of price's diapason
    :type price_up_to: :obj: `int`

    :return: list of the Project class's objects by filter
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_list = create_project_list_by_theme(theme_id)
    return_list = filter_by_prices(price_from, price_up_to, projects_list)

    return return_list


def filter_by_prices(price_from, price_up_to, projects_list):
    if price_from == "None" and price_up_to == "None":
        filtered_list = projects_list
    else:
        filtered_list = filter_list_appending(price_from, price_up_to, projects_list)
    return filtered_list


def filter_list_appending(price_from, price_up_to, projects_list):
    filtered_list = list()
    for project in projects_list:
        if (
            price_from != "None"
            and price_up_to != "None"
            and int(price_from) <= project.price <= int(price_up_to)
        ):
            filtered_list.append(project)
        elif (
            price_from == "None"
            and price_up_to != "None"
            and project.price <= int(price_up_to)
        ):
            filtered_list.append(project)
        elif (
            price_up_to == "None"
            and price_from != "None"
            and project.price >= int(price_from)
        ):
            filtered_list.append(project)
    return filtered_list


def create_project_list_by_theme(themes_id):
    if themes_id != "None":
        projects_list = get_projects_list_by_theme_id(themes_id)
    else:
        projects_list = get_all_project_list()
    return projects_list


def to_parse_project_list(projects_info):
    project_list = list()
    for project_info in projects_info:
        new_project = Project()
        new_project.id = project_info[0][0]
        new_project.seller_id = project_info[0][1]
        new_project.name = project_info[0][2]
        new_project.price = project_info[0][3]
        new_project.status_id = project_info[0][4]
        new_project.subscribers = project_info[0][5]
        new_project.income = project_info[0][6]
        new_project.comment = project_info[0][7]
        new_project.seller_name = project_info[0][8]
        new_project.status = project_info[0][9]
        new_project.vip_ending = project_info[0][12]
        new_project.link = project_info[0][13]
        new_project.is_verified = project_info[0][14]
        for i in range(len(project_info)):
            new_project.themes_id.append(project_info[i][10])
            new_project.themes_names.append(project_info[i][11])
        new_project.params_are_not_none = True
        project_list.append(new_project)
    return project_list


def get_moderator_id():
    """
    This function returns moderator's id from `settings` table.

    :return: id of the moderator
    :rtype: :obj:`int`
    """
    return db_manager.get_settings_info()[0]


def get_guarantee_name():
    """
    This function returns telegram name of the guarantee from `settings` table.

    :return: name of guarantee
    :rtype: :obj:`str`
    """
    return db_manager.get_settings_info()[1]


def get_admin_id():
    """
    This function returns telegram channel id of admin from `settings` table.

    :return: telegram channel name with reviews
    :rtype: :obj:`str`
    """
    return db_manager.get_settings_info()[2]


def get_need_payment():
    """
    This function returns need_payment (0=False, 1=True) from `settings` table.

    :return: 0=False, 1=True
    :rtype: :obj:`int`
    """
    return db_manager.get_settings_info()[3]


def get_regular_sell_price():
    """
    This function returns regular selling price from `settings` table.

    :return: selling price
    :rtype: :obj:`int`
    """
    return db_manager.get_settings_info()[4]


def get_vip_sell_price():
    """
    This function returns vip selling price from `settings` table.

    :return: selling price
    :rtype: :obj:`int`
    """
    return db_manager.get_settings_info()[5]


def get_moderators_info():
    return db_manager.get_all_moderators_info()


def set_current_moderator(moderator_id):
    db_manager.update_current_moderator(moderator_id)


def set_guarantee(guarantee):
    db_manager.update_guarantee(guarantee)


def delete_moderator(moderator_id):
    db_manager.delete_moderator(moderator_id)


def add_moderator(moderator_id, moderator_name):
    db_manager.insert_new_moderator(moderator_id, moderator_name)


def get_all_promo_codes():
    discounts = db_manager.get_discounts()
    promo_list = list()
    for index in range(len(discounts)):
        if discounts[index][1] == 0:
            discount_value = str(discounts[index][2]) + "%"
        else:
            discount_value = str(int(discounts[index][2] / 100)) + "₽"
        promo_list.append(discounts[index][0] + "\t~\t" + discount_value)
    return promo_list


def add_promo_code(new_code, new_discount, new_type):
    if new_type == 1:
        new_discount *= 100
    db_manager.insert_new_promo_code(new_code, new_discount, new_type)


def delete_promo_code(code):
    db_manager.delete_promo_code(code)


def save_regular_price(price):
    db_manager.update_regular_price(price)


def save_vip_price(price):
    db_manager.update_vip_price(price)
