import mysql.connector
from mysql.connector import Error

from config import *
from texts.sql_queries import QUERIES


class DBManager:
    """
    DBManager is class for connection and creating queries to Data Base
    """

    def __init__(self):
        """
        DBManager class constructor.
        Also with initializing DBManager's object a connection is creating.

        :return: Instance of the class
        :rtype: :class:`data_base.db_manager.DBManager`
        """
        self.connection = self.create_connection(HOST, USER, PASSWORD, DATA_BASE)

    @staticmethod
    def create_connection(host_name, user_name, user_password, data_base):
        """
        This function creates connection to the data base.

        :param host_name: host name of data base's server
        :type host_name: :obj: `str`

        :param user_name: user name of data base's server
        :type user_name: :obj: `str`

        :param user_password: user's password of data base's server
        :type user_password: :obj: `str`

        :param data_base: data base's name
        :type data_base: :obj: `str`

        :return: connection to the data base
        :rtype: :class:`MySQLConnection`
        """
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=data_base,
                charset="utf8mb4",
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    @staticmethod
    def get_string_project_values(project):
        """
        Helper function for INSERT or UPDATE queries to `project` table.

        :param project: object of class Project with filled params
        :type project: :class: `data_base.project.Project`

        :return: a part of SQL template for INSERT or UPDATE functions
        :rtype: :obj:`str`
        """
        return (
            str(project.seller_id)
            + ", '"
            + project.name
            + "', "
            + str(project.price)
            + ", "
            + str(project.status_id)
            + ", "
            + str(project.subscribers)
            + ", "
            + str(project.income)
            + ", '"
            + project.comment
            + "', '"
            + str(project.vip_ending)
            + "', '"
            + project.link
            + "', '"
            + str(project.is_verified)
            + "'"
        )

    def insert_project(self, project):
        """
        This function creates INSERT query for new row of `project` table.
        If project's seller does not exist, it will be inserted to the `seller` table.
        Also it inserts rows to intermediate entity `project_theme`.

        :param project: object of class Project with filled params
        :type project: :class: `data_base.project.Project`
        """
        if project.seller_id == -1:
            self.insert_new_seller(project)
            project.seller_id = self.get_seller_id_by_seller_name(project.seller_name)

        project_val = self.get_string_project_values(project)
        create_project = QUERIES["insert_project"] % project_val

        cursor = self.connection.cursor()
        cursor.execute(create_project)
        project_id = cursor.lastrowid
        cursor.close()
        self.insert_project_themes(project_id, project.themes_id)

    def insert_status(self, status_name):
        """
        This function creates INSERT query for new row of `status` table.

        :param status_name: name of new status
        :type status_name: :obj: `str`
        """
        create_status = QUERIES["insert_status"] % status_name
        self.execute_query(self.connection, create_status)

    def insert_theme(self, theme_name):
        """
        This function creates INSERT query for new row of `theme` table.

        :param theme_name: name of new theme
        :type theme_name: :obj: `str`
        """
        create_theme = QUERIES["insert_theme"] % theme_name
        self.execute_query(self.connection, create_theme)

    def insert_project_themes(self, project_id, themes_id):
        """
        This function creates INSERT query for filling new rows of intermediate entity `project_theme`.

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :param themes_id: id of the theme
        :type themes_id: :list: `int`
        """
        for theme_id in themes_id:
            project_theme_val = str(project_id) + ", " + str(theme_id)
            create_project_theme = QUERIES["insert_project_theme"] % project_theme_val
            self.execute_query(self.connection, create_project_theme)

    def insert_new_seller(self, project):
        """
        This function creates INSERT query for new row of `seller` table.

        :param project: object of class Project with filled params
        :type project: :class: `data_base.project.Project`
        """
        seller_val = "'" + project.seller_name + "'"
        create_seller = QUERIES["insert_seller"] % seller_val
        self.execute_query(self.connection, create_seller)

    def insert_new_moderator(self, moderator_id, moderator_name):
        create_moderator = QUERIES["insert_moderator"] % (
            moderator_id + ", '" + moderator_name + "'"
        )
        self.execute_query(self.connection, create_moderator)

    def insert_new_promo_code(self, new_code, new_discount, new_type):
        create_promo = QUERIES["insert_promo_code"] % (
            "'" + new_code + "', " + str(new_discount) + ", " + str(new_type)
        )
        self.execute_query(self.connection, create_promo)

    def is_project_exist_by_id(self, project_id):
        """
        This function checks is project with concrete id exist

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: bool value of existing of the project with concrete id
        :rtype: :obj:`bool`
        """
        get_project_query = QUERIES["select_project_by_id"] % project_id
        project = self.execute_read_query(self.connection, get_project_query)
        if len(project) == 0:
            return False
        else:
            return True

    def get_all_moderators_info(self):
        get_all_moderators_info_query = QUERIES["select_all_moderators_info"]
        moderators = self.execute_read_query(
            self.connection, get_all_moderators_info_query
        )
        return moderators

    def get_seller_name(self, seller_id):
        """
        This function creates SELECT query for getting seller's name of `seller` table by id.

        :param seller_id: id of the project
        :type seller_id: :obj: `int`

        :return: name of the seller with concrete id
        :rtype: :obj:`str`
        """
        get_seller_name_query = QUERIES["select_seller_name_by_seller_id"] % seller_id
        seller_name = self.execute_read_query(self.connection, get_seller_name_query)[
            0
        ][0]
        return seller_name

    def get_seller_id_by_project_id(self, project_id):
        """
        This function creates SELECT query for getting seller's id by project's id.

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: id of the seller of concrete project
        :rtype: :obj:`str`
        """
        get_seller_id_query = QUERIES["select_seller_id_by_project_id"] % project_id
        seller_id = self.execute_read_query(self.connection, get_seller_id_query)[0][0]
        return seller_id

    def is_seller_exist(self, seller_name):
        """
        This function checks if seller exists.

        :param seller_name: id of the project
        :type seller_name: :obj: `int`

        :return: bool value of existing of the seller with concrete name
        :rtype: :obj:`bool`
        """
        get_seller_id_query = QUERIES["select_seller_id_by_seller_name"] % seller_name
        seller_id = self.execute_read_query(self.connection, get_seller_id_query)
        if len(seller_id) == 0:
            return False
        else:
            return True

    def get_seller_id_by_seller_name(self, seller_name):
        """
        This function creates SELECT query for getting seller's id by seller's name.

        :param seller_name: id of the project
        :type seller_name: :obj: `int`

        :return: id of the seller of concrete project
        :rtype: :obj:`str`
        """
        get_seller_id_query = QUERIES["select_seller_id_by_seller_name"] % seller_name
        seller_id = self.execute_read_query(self.connection, get_seller_id_query)[0][0]
        return seller_id

    def get_projects_by_seller_id(self, seller_id):
        """
        This function creates SELECT query for getting all project's info by seller's id.

        :param seller_id: id of the seller
        :type seller_id: :obj: `int`

        :return: list of the projects of the concrete seller
        :rtype: :list::list:`str`
        """
        get_projects_query = QUERIES["select_project_by_seller_id"] % seller_id
        projects = self.execute_read_query(self.connection, get_projects_query)
        return projects

    def get_projects_id_by_seller_name(self, seller_name):
        """
        This function creates SELECT query for getting project's id by seller's name.

        :param seller_name: name of the seller
        :type seller_name: :obj: `str`

        :return: list of the projects with the concrete theme
        :rtype: :list::list:`str`
        """
        get_projects_id_query = QUERIES["select_project_by_seller_name"] % seller_name
        projects_id = self.execute_read_query(self.connection, get_projects_id_query)
        return projects_id

    def get_projects_info_by_seller_name(self, seller_name):
        """
        This function creates SELECT query for getting all project's info by seller's name.

        :param seller_name: name of the seller
        :type seller_name: :obj: `str`

        :return: list of the projects with the concrete theme
        :rtype: :list::list:`str`
        """
        projects_id = self.get_projects_id_by_seller_name(seller_name)
        projects = list()
        for project_id in projects_id:
            projects.append(self.get_all_project_info_by_id(project_id))
        return projects

    def get_projects_info_by_theme_id(self, theme_id):
        """
        This function creates SELECT query for getting all project's info by theme's id.

        :param theme_id: id of the theme
        :type theme_id: :obj: `int`

        :return: list of the projects with the concrete theme
        :rtype: :list::list:`str`
        """
        projects_id = self.get_projects_id_by_theme_id(theme_id)
        projects = list()
        for project_id in projects_id:
            projects.append(self.get_all_project_info_by_id(project_id))
        return projects

    def get_projects_id_by_theme_id(self, theme_id):
        """
        This function creates SELECT query for getting project's id by theme's id.

        :param theme_id: id of the theme
        :type theme_id: :obj: `int`

        :return: list of the projects with the concrete theme
        :rtype: :list::list:`str`
        """
        get_projects_id_query = QUERIES["select_projects_id_by_theme_id"] % theme_id
        projects_id = self.execute_read_query(self.connection, get_projects_id_query)
        return projects_id

    def get_all_project_info_by_id(self, project_id):
        """
        This function creates SELECT query for getting all info about project by project's id
        for filling Project class's object.

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: all project info: id, seller_id, name, price, status_id, subscribers, income,
                    comment, seller_name, status_name, themes_id, themes_name
        :rtype: :list:`str`
        """
        get_project_query = QUERIES["select_all_project_info_by_id"] % project_id
        project = self.execute_read_query(self.connection, get_project_query)

        return project

    def get_moderator_all_projects_id(self):
        """
        This function creates SELECT query for getting all not sorted projects's ids

        :return: ids of the projects
        :rtype: :list:`int`
        """
        get_project_query = QUERIES["select_moderator_all_projects_id"]
        projects_id = self.execute_read_query(self.connection, get_project_query)

        return projects_id

    def get_all_projects_id(self):
        """
        This function creates SELECT query for getting all projects's ids

        :return: ids of the projects
        :rtype: :list:`int`
        """
        get_project_query = QUERIES["select_all_projects_id"]
        projects_id = self.execute_read_query(self.connection, get_project_query)

        return projects_id

    def get_vip_projects_id(self):
        """
        This function creates SELECT query for getting vip projects's ids

        :return: ids of the vip projects
        :rtype: :list:`int`
        """
        get_project_query = QUERIES["select_vip_projects_id"]
        projects_id = self.execute_read_query(self.connection, get_project_query)

        return projects_id

    def get_projects_id_by_prices(self, price_from, price_up_to):
        """
        This function creates SELECT query for getting projects's ids by price filter

        :param price_from: start of price's diapason
        :type price_from: :obj: `int`
        :param price_up_to:end of price's diapason
        :type price_up_to: :obj: `int`

        :return: ids of the projects
        :rtype: :list:`int`
        """
        get_project_query = (
            QUERIES["select_projects_id_by_prices"] % price_from % price_up_to
        )
        projects_id = self.execute_read_query(self.connection, get_project_query)

        return projects_id

    def get_project_by_id(self, project_id):
        """
        This function creates SELECT query for getting info from `project` table by project's id.

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: project's info by the concrete id
        :rtype: :list:`str`
        """
        get_project_query = QUERIES["select_project_by_id"] % project_id
        project = self.execute_read_query(self.connection, get_project_query)[0]
        return project

    def get_themes_names(self, themes_id):
        """
        This function creates SELECT query for getting themes's names by themes's id.

        :param themes_id: list with themes's id
        :type themes_id: :list: `int`

        :return: list with themes's names
        :rtype: :list:`str`
        """
        themes_names = list()
        for theme_id in themes_id:
            get_theme_name_query = QUERIES["select_theme_name_by_theme_id"] % theme_id
            theme_name = self.execute_read_query(self.connection, get_theme_name_query)
            themes_names.append(theme_name[0])
        return themes_names

    def get_themes_id_by_names(self, themes_names):
        """
        This function creates SELECT query for getting themes's id
        from `theme` table by themes's names.

        :param themes_names: list with themes's names
        :type themes_names: :list:`str`

        :return: list with themes's id
        :rtype: :list:`int`
        """
        themes_id = list()
        for theme_name in themes_names:
            get_theme_id_query = QUERIES["select_theme_id_by_theme_name"] % theme_name
            themes_id.append(
                self.execute_read_query(self.connection, get_theme_id_query)[0][0]
            )
        return themes_id

    def get_themes_id(self, project_id):
        """
        This function creates SELECT query for getting themes's id
        from intermediate entity `project_theme` by project's id.

        :param project_id: project's id
        :type project_id: :obj: `int`

        :return: list with themes's id
        :rtype: :list:`int`
        """
        get_theme_id_query = QUERIES["select_themes_id_by_project_id"] % project_id
        themes_id = self.execute_read_query(self.connection, get_theme_id_query)
        return themes_id

    def get_all_themes(self):
        """
        This function creates SELECT query for getting dictionary with all themes
        from `theme` table by themes's names.

        :return: dictionary with themes's info
        :rtype: :dict:`int`:`str`
        """
        get_themes_query = QUERIES["select_all_themes"]
        themes_info = self.execute_read_query(self.connection, get_themes_query)
        return_dict = {}
        for i in range(len(themes_info)):
            return_dict[themes_info[i][0]] = themes_info[i][1]

        return return_dict

    def get_filled_themes(self):
        """
        This function creates SELECT query for getting dictionary with filled themes
        from `theme` table by themes's names.

        :return: dictionary with themes's info
        :rtype: :dict:`int`:`str`
        """
        get_themes_query = QUERIES["select_filled_themes"]
        themes_info = self.execute_read_query(self.connection, get_themes_query)
        return_dict = {}
        for i in range(len(themes_info)):
            return_dict[themes_info[i][0]] = themes_info[i][1]

        return return_dict

    def get_status_name(self, status_id):
        """
        This function creates SELECT query for getting status's name of `status` table by id.

        :param status_id: id of the status
        :type status_id: :obj: `int`

        :return: name of the status with concrete id
        :rtype: :obj:`str`
        """
        get_status_name_query = QUERIES["select_status_name_by_status_id"] % status_id
        status_name = self.execute_read_query(self.connection, get_status_name_query)[
            0
        ][0]
        return status_name

    def get_settings_info(self):
        """
        This function creates SELECT query for getting all settings info from `settings`.

        :return: list of guarantee's name, channel's name of guarantee's reviews and need_payment (0=False, 1=True).
        :rtype: :list:`str`
        """
        get_settings_query = QUERIES["select_all_settings_info"]
        settings_info = self.execute_read_query(self.connection, get_settings_query)[0]
        return settings_info

    def get_discounts(self):
        """
        This function creates SELECT query for getting all discounts info from `discount`.

        :return: code, type (0 - PER CENT, 1 - RUBS), discount
        :rtype: :list:list:`str`
        """
        get_settings_query = QUERIES["select_discounts"]
        discounts = self.execute_read_query(self.connection, get_settings_query)
        return discounts

    def update_project(self, project_id, project):
        """
        This function creates UPDATE query for changing row of `project` table.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`

        :param project: object of class Project with filled params
        :type project: :class: `data_base.project.Project`
        """
        update_project = QUERIES["update_project"] % (
            str(project.seller_id),
            str(project.name),
            str(project.price),
            str(project.status_id),
            str(project.subscribers),
            str(project.income),
            str(project.comment),
            str(project.vip_ending),
            str(project.link),
            str(project.is_verified),
            str(project_id),
        )
        self.update_project_themes(project_id, project.themes_id)
        self.execute_query(self.connection, update_project)

    def update_project_themes(self, project_id, themes_id):
        """
        This function creates UPDATE query for changing row of intermediate entity `project_theme`.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`

        :param themes_id: list with themes's id
        :type themes_id: :list: `int`
        """
        self.delete_project_theme(project_id)
        self.insert_project_themes(project_id, themes_id)

    def update_seller(self, seller_id, seller_name):
        """
        This function creates UPDATE query for changing row of `seller` table.

        :param seller_id: id of existing row of `seller` table
        :type seller_id: :obj: `int`

        :param seller_name: new name of existing seller
        :type seller_name: :obj: `str`
        """
        update_seller = QUERIES["update_seller"] % (seller_name, str(seller_id))
        self.execute_query(self.connection, update_seller)

    def update_current_moderator(self, moderator_id):
        update_moderator = QUERIES["update_current_moderator"] % (str(moderator_id))
        self.execute_query(self.connection, update_moderator)

    def update_guarantee(self, guarantee):
        update_guarantee = QUERIES["update_guarantee"] % guarantee
        self.execute_query(self.connection, update_guarantee)

    def delete_moderator(self, moderator_id):
        delete_moderator = QUERIES["delete_moderator"] % (str(moderator_id))
        self.execute_query(self.connection, delete_moderator)

    def delete_project(self, project_id):
        """
        This function creates DELETE query for deleting row from `project` and `project_theme` tables.
        Also if current project's seller will have no projects anymore,
        row from `seller` table with his id will be deleted too.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`
        """
        self.delete_project_theme(project_id)
        delete_project_query = QUERIES["delete_project"] % (str(project_id))
        seller_id = self.get_seller_id_by_project_id(project_id)
        self.execute_query(self.connection, delete_project_query)
        projects = self.get_projects_by_seller_id(seller_id)
        if len(projects) == 0:
            self.delete_seller(seller_id)

    def delete_seller(self, seller_id):
        """
        This function creates DELETE query for deleting row from `seller` table.

        :param seller_id: id of existing row of `seller` table
        :type seller_id: :obj: `int`
        """
        delete_seller_query = QUERIES["delete_seller"] % (str(seller_id))
        self.execute_query(self.connection, delete_seller_query)

    def delete_project_theme(self, project_id):
        """
        This function creates DELETE query for deleting all rows
        from intermediate entity `project_theme` with project id.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`
        """
        delete_project_theme_query = QUERIES["delete_project_theme"] % (str(project_id))
        self.execute_query(self.connection, delete_project_theme_query)

    @staticmethod
    def execute_query(connection, query):
        """
        This function executes SQL INSERT, UPDATE and DELETE queries to data base.

        :param connection: connection to the data base
        :type connection: :class:`MySQLConnection`

        :param query: string query to the data base
        :type query: :obj:`str`
        """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def execute_read_query(connection, query):
        """
        This function executes SQL SELECT queries to data base.

        :param connection: connection to the data base
        :type connection: :class:`MySQLConnection`

        :param query: string query to the data base
        :type query: :obj:`str`

        :return: issue sheet on SQL query
        :rtype: :list::list:`str`
        """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
