from useful.instruments import db_manager


class Discount:
    """
    Data class for convenient work with Data Base's table `discount`
    """

    def __init__(self):
        self.code = None
        self.type = None
        self.discount = None

    def use_discount(self, code, price):
        new_price = price
        discount_list = db_manager.get_discounts()
        if len(discount_list) != 0:
            for discount in discount_list:
                if discount[0] == code:
                    self._set_discount(discount)
                    new_price = self._get_new_price(price)
        return int(new_price)

    def _set_discount(self, discount):
        self.code = discount[0]
        self.type = discount[1]
        self.discount = int(discount[2])

    def _get_new_price(self, price):
        if self.type == 0:
            return price - price * self.discount / 100
        elif self.type == 1:
            return price - self.discount
        else:
            return price
