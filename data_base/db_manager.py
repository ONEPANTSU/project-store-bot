import mysql.connector
from mysql.connector import Error
from config import *

class DBManager():

    def __init__(self):
        self.connection = self.create_connection(HOST, USER, PASSWORD, DATA_BASE)

    def create_connection(self, host_name, user_name, user_password, data_base):
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

    def insert_project(self, project):
        project_val = str(project.seller_id) + ", '" + project.name + "', " +  str(project.price)  + ", " + \
                      str(project.status_id) + ", " + str(project.subscribers) + ", " + \
                      str(project.income) + ", '" +  project.comment + "'"
        create_project = """
        INSERT INTO
        `project` (`seller_id`, `name`, `price`, `status_id`, `subscribers`, `income`, `comment`)
        VALUES
        (%s);
        """ % (project_val)
        select_current_seller = "SELECT * FROM `seller` WHERE `id` = '%s';" % (project.seller_id)
        current_seller = self.execute_read_query(self.connection, select_current_seller)
        if(len(current_seller) == 0):
            self.insert_new_seller(project)
        #self.execute_query(self.connection, create_project)
        cursor = self.connection.cursor()
        cursor.execute(create_project)
        project_id = cursor.lastrowid
        cursor.close()
        self.insert_project_themes(project_id, project.themes_id)


    def insert_status(self, status_name):
        create_status = """
        INSERT INTO
        `status` (`status_name`)
        VALUES
        (%s);
        """ % (status_name)
        self.execute_query(self.connection, create_status)

    def insert_theme(self, theme_name):
        create_theme = """
        INSERT INTO
        `theme` (`theme_name`)
        VALUES
        (%s);
        """ % (theme_name)
        self.execute_query(self.connection, create_theme)

    def insert_project_themes(self, project_id, themes_id):
        for theme_id in themes_id:
            project_theme_val = str(project_id) + ", " + str(theme_id[0])
            create_project_theme = """
            INSERT INTO
            `project_theme` (`project_id`, `theme_id`)
            VALUES
            (%s);
            """ % (project_theme_val)
            self.execute_query(self.connection, create_project_theme)

    def insert_new_seller(self, project):
        seller_val = "'" + project.seller + "'"
        create_seller = """
        INSERT INTO
        `seller` (`telegram_name`)
        VALUES
        (%s);
        """ % (seller_val)
        self.execute_query(self.connection, create_seller)

    def is_project_exists_by_id(self, project_id):
        get_project_query = "SELECT * FROM `project` WHERE `id` = '%s';" % (project_id)
        project = self.execute_read_query(self.connection, get_project_query)
        if len(project) == 0:
            return False
        else:
            return True

    def get_seller_name(self, seller_id):
        get_seller_name_query = "SELECT `telegram_name` FROM `seller` WHERE `id` = '%s';" % (seller_id)
        seller_name = self.execute_read_query(self.connection, get_seller_name_query)[0][0]
        return seller_name

    def get_seller_id(self, project_id):
        get_seller_id_query = "SELECT `seller_id` FROM `project` WHERE `id` = '%s';" % (project_id)
        seller_id = self.execute_read_query(self.connection, get_seller_id_query)[0][0]
        return seller_id

    def get_projects_by_seller_id(self, seller_id):
        get_projects_query = "SELECT * FROM `project` WHERE `seller_id` = '%s';" % (seller_id)
        projects = self.execute_read_query(self.connection, get_projects_query)
        return projects

    def get_project_by_id(self, project_id):
        get_project_query = "SELECT * FROM `project` WHERE `id` = '%s';" % (project_id)
        project = self.execute_read_query(self.connection, get_project_query)[0]
        return project

    def get_themes_names(self, themes_id):
        themes_names = list()
        for theme_id in themes_id:
            get_theme_name_query = "SELECT `theme_name` FROM `theme` WHERE `id` = '%s';" % (theme_id)
            theme_name = self.execute_read_query(self.connection, get_theme_name_query)
            themes_names.append(theme_name[0])
        return themes_names

    def get_themes_id(self, project_id):
        get_theme_id_query = "SELECT `theme_id` FROM `project_theme` WHERE `project_id` = '%s';" % (project_id)
        themes_id = self.execute_read_query(self.connection, get_theme_id_query)
        return themes_id

    def get_status_name(self, status_id):
        get_status_name_query = "SELECT `status_name` FROM `status` WHERE `id` = '%s';" % (status_id)
        status_name = self.execute_read_query(self.connection, get_status_name_query)[0][0]
        return status_name

    def get_guarantee_info(self):
        get_guarantee_query = "SELECT * FROM `guarantee`;"
        guarantee_info = self.execute_read_query(self.connection, get_guarantee_query)[0]
        return guarantee_info

    def update_project(self, project_id, project):
        project_val = str(project.seller_id) + ", '" + project.name + "', " + str(project.price) + ", " + \
                      str(project.status_id) + ", " + str(project.subscribers) + ", " + \
                      str(project.income) + ", '" + project.comment + "'"
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
        self.delete_project_theme(project_id)
        self.insert_project_themes(project_id, themes_id)

    def update_seller(self, seller_id, seller_name):
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
        self.delete_project_theme(project_id)
        delete_project_query = "DELETE FROM `project` WHERE `id` = `%s`;" % (str(project_id))
        seller_id = self.get_seller_id(project_id)
        projects = self.get_projects_by_seller_id(seller_id)
        if(len(projects) == 0):
            self.delete_seller(seller_id)
        self.execute_query(self.connection, delete_project_query)

    def delete_seller(self, seller_id):
        delete_seller_query = "DELETE FROM `seller` WHERE `id` = `%s`;" % (str(seller_id))
        self.execute_query(self.connection, delete_seller_query)

    def delete_project_theme(self, project_id):
        delete_project_theme_query = "DELETE FROM `project_theme` WHERE `project_id` = `%s`;" % (str(project_id))
        self.execute_query(self.connection, delete_project_theme_query)

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
