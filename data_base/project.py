from data_base.db_manager import DBManager


class Project:
    """
    Data class for convenient work with Data Base's tables
    """

    def __init__(self):
        """
        Project class constructor

        :return: Instance of the class
        :rtype: :class:`data_classes.project.Project`
        """
        self.db_manager = DBManager()

        self.params_are_not_none = False
        self.id = None
        self.seller_id = None
        self.seller_name = None
        self.name = None
        self.themes_id = None
        self.themes_names = None
        self.price = None
        self.status_id = None
        self.status = None
        self.subscribers = None
        self.income = None
        self.comment = None

    def set_params(self, seller_id, name,
                   price, status_id, subscribers,
                   themes_id, income, comment):
        """
        This function sets values of all params to the Project's object.
        It is necessary for filling all columns in the row of data base.

        :param seller_id: ID of seller table's row
        :type seller_id: :obj: `int`

        :param name: name of the project
        :type name: :obj: `str`

        :param price: price of the project (rubles)
        :type price: :obj: `int`

        :param status_id: status ID of status enum
        :type status_id: :obj: `int`

        :param subscribers: count of subscribers
        :type subscribers: :obj: `int`

        :param themes_id: list of themes id
        :type themes_id: :list: `int`

        :param income: income from the project (rubles)
        :type income: :obj: `int`

        :param comment: project description and comment
        :type comment: :obj: `str`
        """

        self.params_are_not_none = True

        self.seller_id = seller_id
        self.seller_name = self.db_manager.get_seller_name(seller_id)
        self.name = name
        self.themes_id = themes_id
        self.themes_names = self.db_manager.get_themes_names(themes_id)
        self.price = price
        self.status_id = status_id
        self.status = self.db_manager.get_status_name(status_id)
        self.subscribers = subscribers
        self.income = income
        self.comment = comment

    def set_params_by_id(self, project_id):
        """
        This function sets values of all searched params to the Project's object.
        The search is carried out by the id of the existing project.

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.set_id(project_id)
        if self.db_manager.is_project_exists_by_id(self.id):
            project_sql_row = self.db_manager.get_project_by_id(self.id)
            themes_id = self.db_manager.get_themes_id(self.id)
            self.set_params(seller_id=project_sql_row[1], name=project_sql_row[2], price=project_sql_row[3],
                            status_id=project_sql_row[4], subscribers=project_sql_row[5], income=project_sql_row[6],
                            comment=project_sql_row[7], themes_id=themes_id)
        else:
            print("Error: Project does not exist")

    def set_id(self, project_id):
        """
        This function sets concrete id to the Project's object
        It is necessary in cases of searching of existing projects

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.id = project_id

    def save_new_project(self):
        """
        This function inserts filled params of the Project's object to the new row of the data base.
        """
        if self.params_are_not_none is False:
            print("Error: Project's params are empty")
        else:
            self.db_manager.insert_project(self)

    def save_changes_to_existing_project(self):
        """
        This function updates already existing row of data base by new params of the Project's object.
        """
        if self.params_are_not_none is False:
            print("Error: Project's params are empty")
        elif self.id is None:
            print("Error: Project's id is empty")
        else:
            self.db_manager.update_project(self.id, self)

    def delete_project_by_id(self, project_id):
        """
        This function deletes existing row of data base by id of the Project's object.

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.set_id(project_id)
        if self.db_manager.is_project_exists_by_id(self.id):
            self.db_manager.delete_project(self.id)
        else:
            print("Error: Project does not exist")

    def get_guarantee_name(self):
        """
        This function returns telegram name of the guarantee from `guarantee` table.

        :return: name of guarantee
        :rtype: :obj:`str`
        """
        guarantee_name = self.db_manager.get_guarantee_info()[0]
        return guarantee_name

    def get_guarantee_reviews(self):
        """
        This function returns telegram channel name with reviews of the guarantee from `guarantee` table.

        :return: telegram channel name with reviews
        :rtype: :obj:`str`
        """
        guarantee_reviews = self.db_manager.get_guarantee_info()[1]
        return guarantee_reviews
