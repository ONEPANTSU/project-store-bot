from instruments import db_manager


def get_guarantee_name():
    """
    This function returns telegram name of the guarantee from `guarantee` table.

    :return: name of guarantee
    :rtype: :obj:`str`
    """
    guarantee_name = db_manager.get_guarantee_info()[0]
    return guarantee_name


def get_guarantee_reviews():
    """
    This function returns telegram channel name with reviews of the guarantee from `guarantee` table.

    :return: telegram channel name with reviews
    :rtype: :obj:`str`
    """
    guarantee_reviews = db_manager.get_guarantee_info()[1]
    return guarantee_reviews


class Project:
    """
    Data class for convenient work with Data Base's tables
    """

    def __init__(self):
        """
        Project class constructor.

        :return: Instance of the class
        :rtype: :class:`data_base.project.Project`
        """

        self.params_are_not_none = False
        self.id = None
        self.seller_id = None
        self.seller_name = None
        self.name = None
        self.themes_id = list()
        self.themes_names = list()
        self.price = None
        self.status_id = None
        self.status = None
        self.subscribers = None
        self.income = None
        self.comment = None

    def set_params(self, seller_id, seller_name, name,
                   price, status_id, subscribers,
                   themes_id, income, comment):
        """
        This function sets values of all params to the Project's object.
        It is necessary for filling all columns in the row of data base.

        :param seller_id: ID of seller table's row
        :type seller_id: :obj: `int`

        :param seller_name: name of the seller
        :type seller_name: :obj: `str`

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

        self.name = name
        self.themes_id = themes_id
        self.themes_names = db_manager.get_themes_names(themes_id)
        self.price = price
        self.status_id = status_id
        self.status = db_manager.get_status_name(status_id)
        self.subscribers = subscribers
        self.income = income # доход в месяц
        self.comment = comment

        if seller_name is not None:
            if db_manager.is_seller_exist(seller_name):
                self.seller_id = db_manager.get_seller_id_by_seller_name(seller_name)
            else:
                self.seller_id = -1
            self.seller_name = seller_name
        elif seller_id is not None:
            self.seller_id = seller_id
            self.seller_name = db_manager.get_seller_name(seller_id)
        else:
            print("Error! Seller's info is empty!")

    def set_params_by_id(self, project_id):
        """
        This function sets values of all searched params to the Project's object.
        The search is carried out by the id of the existing project.

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.set_id(project_id)
        if db_manager.is_project_exist_by_id(self.id):
            project_sql_row = db_manager.get_project_by_id(self.id)
            themes_id = db_manager.get_themes_id(self.id)
            self.set_params(seller_id=project_sql_row[1], seller_name=None, name=project_sql_row[2],
                            price=project_sql_row[3],
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
        self.check_is_not_none()
        if self.params_are_not_none is False:
            print("Error: Project's params are empty")
        else:
            db_manager.insert_project(self)

    def check_is_not_none(self):
        """
        This function checks "params_are_not_none" variable.
        """
        if self.status is None and self.status_id is not None:
            self.status = db_manager.get_status_name(self.status_id)

        if self.seller_name is not None:
            if db_manager.is_seller_exist(self.seller_name):
                self.seller_id = db_manager.get_seller_id_by_seller_name(self.seller_name)
            else:
                self.seller_id = -1

        if len(self.themes_names) == 0 and len(self.themes_id) != 0:
            self.themes_names = db_manager.get_themes_names(self.themes_id)
        elif len(self.themes_id) == 0 and len(self.themes_names) != 0:
            self.themes_id = db_manager.get_themes_id_by_names(self.themes_names)

        if self.name is not None and self.seller_name is not None and self.seller_id is not None and \
                self.price is not None and self.status_id is not None and len(self.themes_id) != 0 and \
                self.income is not None and self.comment is not None:
            self.params_are_not_none = True
        else:
            self.params_are_not_none = False

    def save_changes_to_existing_project(self):
        """
        This function updates already existing row of data base by new params of the Project's object.
        """
        if self.params_are_not_none is False:
            print("Error: Project's params are empty")
        elif self.id is None:
            print("Error: Project's id is empty")
        else:
            db_manager.update_project(self.id, self)

    def delete_project_by_id(self, project_id):
        """
        This function deletes existing row of data base by id of the Project's object.

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.set_id(project_id)
        if db_manager.is_project_exist_by_id(self.id):
            db_manager.delete_project(self.id)
        else:
            print("Error: Project does not exist")


def get_projects_list_by_theme_id(theme_id):
    """
    This function creates SELECT query for getting all Project class's objects by theme's id.

    :param theme_id: id of the theme
    :type theme_id: :obj: `int`

    :return: list of the Project class's objects with the concrete theme
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_info = db_manager.get_projects_info_by_theme_id(theme_id)
    return to_parse_project_list(projects_info)


def get_projects_list_by_themes_id(themes_id):
    """
    This function creates SELECT query for getting all Project class's objects by themes's id.

    :param themes_id: list with id of the themes
    :type themes_id: :list: `int`

    :return: list of the Project class's objects with the concrete theme
    :rtype: :list::class:`data_base.project.Project`
    """
    projects_list = list()
    for theme_id in themes_id:
        projects_list = projects_list + get_projects_list_by_theme_id(theme_id)
    id_list = list()
    for element in projects_list:
        if element.id in id_list:
            projects_list.remove(element)
        else:
            id_list.append(element.id)
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
    projects_list = to_parse_project_list(projects_info)
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
        for i in range(len(project_info)):
            new_project.themes_id.append(project_info[i][10])
            new_project.themes_names.append(project_info[i][11])
        new_project.params_are_not_none = True
        project_list.append(new_project)
    return project_list
