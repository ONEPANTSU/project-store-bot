from data_classes.status import Status
from data_classes.theme import Theme

class Project:
    """
    Data class for project table of Data Base

    :param id: ID of project table's row
    :type id: :obj: `int`

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

    :param rub_per_sub: count of rubles per subscriber (rubles)
    :type rub_per_sub: :obj: `int`

    :param income: income from the project (rubles)
    :type income: :obj: `int`

    :param comment: project description and comment
    :type id: :obj: `str`

    :param views: count of views
    :type id: :obj: `int`

    :return: Instance of the class
    :rtype: :class:`data_classes.project.Project`
    """

    def __init__(self, seller_id, name,
                 price, status_id, subscribers,
                 rub_per_sub, income, comment, views):
        self.seller_id = seller_id
        self.seller = self.find_seller_by_seller_id()
        self.name = name
        self.themes = self.find_themes_by_id()
        self.price = price
        self.status_id = status_id
        self.status = Status(status_id)
        self.subscribers = subscribers
        self.rub_per_sub = rub_per_sub
        self.income = income
        self.comment = comment
        self.views = views

    def find_seller_by_seller_id(self):
        seller = ""
        #
        return seller

    def find_themes_by_id(self):
        themes = list()

        #   theme = Theme(index)
        #   themes.append(theme)

        return themes

    def add_new_project_to_DB(self):
        pass

    def change_project_in_DB_by_id(self):
        pass

    def delete_project_from_DB_by_id(self):
        pass

def get_project_by_id(id):
    pass

