from abc import ABCMeta, abstractmethod


class API(metaclass=ABCMeta):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_market_snapshot(self, codes):
        """
        :param codes: set type, tells which stocks or coins are required
        :return: map<code, tuple(last_price, update_timestamp, update_local_time)>
            update_local_time format: %Y-%m-%d %H:%M:%S
        """
        pass

    # get_pre_trade_info is used for checking before submitting an order,
    # we need to know how many stocks or coins at most we can buy or sell.
    # return pre-trade info (dict with keys: DICT_KEY_MAX_BUY, DICT_KEY_MAX_SELL)
    @abstractmethod
    def get_pre_trade_info(self, code, price):
        pass

    # get_orders is used for checking order before submitting an order,
    # return orders as list type: [<order1>, <order2>, ...]
    @abstractmethod
    def get_orders(self, code, trade_side, order_status):
        """
        :return: order list by order ID in descending order
            [<order X>, <order X-1>, ...]
            order format: (order_id, status, create_timestamp, update_timestamp, trade_side,
                            submit_price, submit_num, filled_avg_price, filled_num)
        """
        pass

    # get status and avg price for specified order
    def get_order_status_and_price(self, code, order_id):
        """
        :return: (order_status, price) (tuple)
        """
        pass

    # place order for specified code, return None if something wrong happened.
    @abstractmethod
    def place_order(self, code, price, number, order_type, trade_side):
        """
        :return: new_order_id
        """
        pass

    @abstractmethod
    def cancel_order(self, code, order_id):
        """
        :return: is_succeed (bool)
        """
        pass
