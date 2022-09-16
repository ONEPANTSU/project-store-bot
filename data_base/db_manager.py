import mysql.connector
from mysql.connector import Error
from data_classes.project import Project
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

    def insert_to_db(self, project):
        project_val = str(project.seller_id) + ", '" + project.name + "', " +  str(project.price)  + ", " + \
                      str(project.status_id) + ", " + str(project.subscribers) + ", " + str(project.rub_per_sub) + ", " + \
                      str(project.income) + ", '" +  project.comment + "', " + str(project.views)

        create_project = """
        INSERT INTO
        `project` (`seller_id`, `name`, `price`, `status_id`, `subscribers`, `rub_per_sub`, `income`, `comment`, `views`)
        VALUES
        (%s);
        """ % (project_val)

        seller_val = str(project.seller_id) + ", '" + project.seller + "'"

        create_seller = """
        INSERT INTO
        `seller` (`id`, `telegram_name`)
        VALUES
        (%s);
        """ % (seller_val)

        self.execute_query(self.connection, create_seller)

        self.execute_query(self.connection, create_project)

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

# project = Project(seller_id=3, name="Channel",
#                  price=100, status_id=0, subscribers=20,
#                  rub_per_sub=1, income=20, comment="Super channel. Just buy it!", views=30)
# project.seller = "@onepanstu"
#
# db_manager = DBManager()
# db_manager.insert_to_db(project)