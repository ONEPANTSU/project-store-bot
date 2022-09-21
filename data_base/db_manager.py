import mysql.connector
from mysql.connector import Error
from config import *


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
                database=data_base
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
        return str(project.seller_id) + ", '" + project.name + "', " + str(project.price) + ", " + \
               str(project.status_id) + ", " + str(project.subscribers) + ", " + \
               str(project.income) + ", '" + project.comment + "'"

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
        create_project = """
        INSERT INTO
        `project` (`seller_id`, `name`, `price`, `status_id`, `subscribers`, `income`, `comment`)
        VALUES
        (%s);
        """ % project_val

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
        create_status = """
        INSERT INTO
        `status` (`status_name`)
        VALUES
        (%s);
        """ % status_name
        self.execute_query(self.connection, create_status)

    def insert_theme(self, theme_name):
        """
        This function creates INSERT query for new row of `theme` table.

        :param theme_name: name of new theme
        :type theme_name: :obj: `str`
        """
        create_theme = """
        INSERT INTO
        `theme` (`theme_name`)
        VALUES
        (%s);
        """ % theme_name
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
            create_project_theme = """
            INSERT INTO
            `project_theme` (`project_id`, `theme_id`)
            VALUES
            (%s);
            """ % project_theme_val
            self.execute_query(self.connection, create_project_theme)

    def insert_new_seller(self, project):
        """
        This function creates INSERT query for new row of `seller` table.

        :param project: object of class Project with filled params
        :type project: :class: `data_base.project.Project`
        """
        seller_val = "'" + project.seller_name + "'"
        create_seller = """
        INSERT INTO
        `seller` (`telegram_name`)
        VALUES
        (%s);
        """ % seller_val
        self.execute_query(self.connection, create_seller)

    def is_project_exist_by_id(self, project_id):
        """
        This function checks is project with concrete id exist

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: bool value of existing of the project with concrete id
        :rtype: :obj:`bool`
        """
        get_project_query = "SELECT * FROM `project` WHERE `id` = '%s';" % project_id
        project = self.execute_read_query(self.connection, get_project_query)
        if len(project) == 0:
            return False
        else:
            return True

    def get_seller_name(self, seller_id):
        """
        This function creates SELECT query for getting seller's name of `seller` table by id.

        :param seller_id: id of the project
        :type seller_id: :obj: `int`

        :return: name of the seller with concrete id
        :rtype: :obj:`str`
        """
        get_seller_name_query = "SELECT `telegram_name` FROM `seller` WHERE `id` = '%s';" % seller_id
        seller_name = self.execute_read_query(self.connection, get_seller_name_query)[0][0]
        return seller_name

    def get_seller_id_by_project_id(self, project_id):
        """
        This function creates SELECT query for getting seller's id by project's id.

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: id of the seller of concrete project
        :rtype: :obj:`str`
        """
        get_seller_id_query = "SELECT `seller_id` FROM `project` WHERE `id` = '%s';" % project_id
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
        get_seller_id_query = "SELECT `id` FROM `seller` WHERE `telegram_name` = '%s';" % seller_name
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
        get_seller_id_query = "SELECT `id` FROM `seller` WHERE `telegram_name` = '%s';" % seller_name
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
        get_projects_query = "SELECT * FROM `project` WHERE `seller_id` = '%s';" % seller_id
        projects = self.execute_read_query(self.connection, get_projects_query)
        return projects

    def get_project_by_id(self, project_id):
        """
        This function creates SELECT query for getting project's info by project's id.

        :param project_id: id of the project
        :type project_id: :obj: `int`

        :return: project's info by the concrete id
        :rtype: :list:`str`
        """
        get_project_query = "SELECT * FROM `project` WHERE `id` = '%s';" % project_id
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
            get_theme_name_query = "SELECT `theme_name` FROM `theme` WHERE `id` = '%s';" % theme_id
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
        for theme in themes_names:
            get_theme_id_query = "SELECT `id` FROM `theme` WHERE `theme_name` = '%s';" % theme
            themes_id.append(self.execute_read_query(self.connection, get_theme_id_query)[0][0])
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
        get_theme_id_query = "SELECT `theme_id` FROM `project_theme` WHERE `project_id` = '%s';" % project_id
        themes_id = self.execute_read_query(self.connection, get_theme_id_query)
        return themes_id

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
        for theme in themes_names:
            get_theme_id_query = "SELECT `id` FROM `theme` WHERE `theme_name` = '%s';" % theme
            themes_id.append(self.execute_read_query(self.connection, get_theme_id_query)[0][0])
        return themes_id

    def get_all_themes(self):
        """
        This function creates SELECT query for getting dictionary with all themes
        from `theme` table by themes's names.

        :return: dictionary with themes's info
        :rtype: :dict:`int`:`str`
        """
        get_themes_query = "SELECT * FROM `theme`;"
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
        get_status_name_query = "SELECT `status_name` FROM `status` WHERE `id` = '%s';" % status_id
        status_name = self.execute_read_query(self.connection, get_status_name_query)[0][0]
        return status_name

    def get_guarantee_info(self):
        """
        This function creates SELECT query for getting all guarantee info from of `guarantee`.

        :return: list of guarantee's name and channel's name of guarantee's reviews.
        :rtype: :list:`str`
        """
        get_guarantee_query = "SELECT * FROM `guarantee`;"
        guarantee_info = self.execute_read_query(self.connection, get_guarantee_query)[0]
        return guarantee_info

    def update_project(self, project_id, project):
        """
        This function creates UPDATE query for changing row of `project` table.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`

        :param project: object of class Project with filled params
        :type project: :class: `data_base.project.Project`
        """
        project_val = self.get_string_project_values(project)
        update_project = """
        UPDATE
        `project` (`seller_id`, `name`, `price`, `status_id`, `subscribers`, `income`, `comment`)
        SET
        (%s)
        WHERE `id` = `%s`;
        """ % (project_val, str(project_id))
        self.update_project_themes(project_id, project.themes)
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
        seller_val = "'" + seller_name + "'"
        update_seller = """
        UPDATE
        `seller` (`telegram_name`)
        SET
        (%s)
        WHERE `id` = `%s`;
        """ % (seller_val, str(seller_id))
        self.execute_query(self.connection, update_seller)

    def delete_project(self, project_id):
        """
        This function creates DELETE query for deleting row from `project` and `project_theme` tables.
        Also if current project's seller will have no projects anymore,
        row from `seller` table with his id will be deleted too.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`
        """
        self.delete_project_theme(project_id)
        delete_project_query = "DELETE FROM `project` WHERE `id` = `%s`;" % (str(project_id))
        seller_id = self.get_seller_id(project_id)
        projects = self.get_projects_by_seller_id(seller_id)
        if len(projects) == 0:
            self.delete_seller(seller_id)
        self.execute_query(self.connection, delete_project_query)

    def delete_seller(self, seller_id):
        """
        This function creates DELETE query for deleting row from `seller` table.

        :param seller_id: id of existing row of `seller` table
        :type seller_id: :obj: `int`
        """
        delete_seller_query = "DELETE FROM `seller` WHERE `id` = `%s`;" % (str(seller_id))
        self.execute_query(self.connection, delete_seller_query)

    def delete_project_theme(self, project_id):
        """
        This function creates DELETE query for deleting all rows
        from intermediate entity `project_theme` with project id.

        :param project_id: id of existing row of `project` table
        :type project_id: :obj: `int`
        """
        delete_project_theme_query = "DELETE FROM `project_theme` WHERE `project_id` = `%s`;" % (str(project_id))
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