from useful.instruments import db_manager


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
        self.vip_ending = None
        self.link = None
        self.is_verified = 0

    def set_params(
        self,
        seller_id,
        seller_name,
        name,
        price,
        status_id,
        subscribers,
        themes_id,
        income,
        comment,
        vip_ending,
        link,
        is_verified,
    ):
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

        :param vip_ending: vip subscription expiration date
        :type vip_ending: :obj: `datetime`

        :param link: link to project
        :type link: :obj: `str`

        :param is_verified: 1 - YES, 0 - NO
        :type is_verified: :obj: `int`
        """

        self.params_are_not_none = True

        self.name = name
        self.themes_id = themes_id
        self.themes_names = db_manager.get_themes_names(themes_id)
        self.price = price
        self.status_id = status_id
        self.status = db_manager.get_status_name(status_id)
        self.subscribers = subscribers
        self.income = income  # доход в месяц
        self.comment = comment
        self._set_seller_info(seller_name, seller_id)
        self.vip_ending = vip_ending  # дата окончания вип-подписки
        self.link = link
        self.is_verified = is_verified

    def _set_seller_info(self, seller_name, seller_id):
        if seller_name is not None:
            self._set_seller_info_by_name(seller_name)
        elif seller_id is not None:
            self._set_seller_info_by_id(seller_id)
        else:
            print("Error! Seller's info is empty!")

    def _set_seller_info_by_id(self, seller_id):
        self.seller_id = seller_id
        self.seller_name = db_manager.get_seller_name(seller_id)

    def _set_seller_info_by_name(self, seller_name):
        if db_manager.is_seller_exist(seller_name):
            self.seller_id = db_manager.get_seller_id_by_seller_name(seller_name)
        else:
            self.seller_id = -1
        self.seller_name = seller_name

    def set_params_by_id(self, project_id):
        """
        This function sets values of all searched params to
        the Project's object.
        The search is carried out by the id of the existing project.

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.set_id(project_id)
        if db_manager.is_project_exist_by_id(self.id):
            self._set_exist_params()
        else:
            print("Error: Project does not exist")

    def _set_exist_params(self):
        project_sql_row = db_manager.get_project_by_id(self.id)
        themes_id = db_manager.get_themes_id(self.id)
        for index in range(len(themes_id)):
            themes_id[index] = themes_id[index][0]
        self.set_params(
            seller_id=project_sql_row[1],
            seller_name=None,
            name=project_sql_row[2],
            price=project_sql_row[3],
            status_id=project_sql_row[4],
            subscribers=project_sql_row[5],
            income=project_sql_row[6],
            comment=project_sql_row[7],
            themes_id=themes_id,
            vip_ending=project_sql_row[8],
            link=project_sql_row[9],
            is_verified=project_sql_row[10],
        )

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
        This function inserts filled params of
        the Project's object to the new row of the data base.
        """
        self._check_is_not_none()
        if self.params_are_not_none:
            db_manager.insert_project(self)
        else:
            print("Error: Project's params are empty")

    def _check_is_not_none(self):
        """
        This function checks "params_are_not_none" variable.
        """
        self._check_coupled_params()
        self._set_params_are_not_none()

    def _check_coupled_params(self):
        self._check_status()
        self._check_seller()
        self._check_themes()

    def _set_params_are_not_none(self):
        if (
            self.name is not None
            and self.seller_name is not None
            and self.seller_id is not None
            and self.price is not None
            and self.status_id is not None
            and len(self.themes_id) != 0
            and self.income is not None
            and self.comment is not None
            and self.vip_ending is not None
            and self.link is not None
            and self.is_verified is not None
        ):
            self.params_are_not_none = True
        else:
            self.params_are_not_none = False

    def _check_themes(self):
        if len(self.themes_names) == 0 and len(self.themes_id) != 0:
            self.themes_names = db_manager.get_themes_names(self.themes_id)
        elif len(self.themes_id) == 0 and len(self.themes_names) != 0:
            self.themes_id = db_manager.get_themes_id_by_names(self.themes_names)

    def _check_seller(self):
        if self.seller_name is not None:
            if db_manager.is_seller_exist(self.seller_name):
                self.seller_id = db_manager.get_seller_id_by_seller_name(
                    self.seller_name
                )
            else:
                self.seller_id = -1

    def _check_status(self):
        if self.status is None and self.status_id is not None:
            self.status = db_manager.get_status_name(self.status_id)

    def save_changes_to_existing_project(self):
        """
        This function updates already existing row of
        data base by new params of the Project's object.
        """

        self._check_is_not_none()
        if self.params_are_not_none is False:
            print("Error: Project's params are empty")
        elif self.id is None:
            print("Error: Project's id is empty")
        else:
            db_manager.update_project(self.id, self)

    def delete_project_by_id(self, project_id):
        """
        This function deletes existing row of
        data base by id of the Project's object.

        :param project_id: ID of project table's row
        :type project_id: :obj: `int`
        """
        self.set_id(project_id)
        if db_manager.is_project_exist_by_id(self.id):
            db_manager.delete_project(self.id)
        else:
            print("Error: Project does not exist")
