import futu
import logging
from pyqt.api import interface, constants
from pyqt.utils.time import *


class FutuAPI(interface.API):

    def __init__(self, host, port, pwd_unlock, local_timezone='Asia/Shanghai',
                 code_prefix_to_timezone_mapping={'US': 'America/New_York'},
                 enable_quote_handler=False, enable_rt_handler=False):
        self.host = host
        self.port = port
        self.pwd_unlock = pwd_unlock
        self.trd_ctx = None
        self.enable_quote_handler = enable_quote_handler
        self.quote_handler = None
        self.enable_rt_handler = enable_rt_handler
        self.rt_handler = None
        self.order_status_map = dict()
        self.subscribe_codes = []
        self.quote_contexts_4_quote = dict()
        self.quote_ctx = None
        self.local_timezone = local_timezone
        self.code_prefix_to_timezone_mapping = code_prefix_to_timezone_mapping

    def initialize_if_not_started(self):
        if not self.trd_ctx or not self.quote_ctx:
            logging.info("initializing FuTu API...")
            self.trd_ctx = futu.OpenUSTradeContext(host=self.host, port=self.port)
            self.trd_ctx.unlock_trade(self.pwd_unlock)
            self.quote_ctx = futu.OpenQuoteContext(host=self.host, port=self.port)
            logging.info("initialized FuTu API!")

    def start(self):
        pass

    def stop(self):
        if self.trd_ctx:
            self.trd_ctx.close()
        if self.quote_ctx:
            self.quote_ctx.close()

    def get_trade_context(self):
        if not self.trd_ctx:
            self.initialize_if_not_started()
        return self.trd_ctx

    def get_quote_context(self):
        if not self.quote_ctx:
            self.initialize_if_not_started()
        return self.quote_ctx

    def set_rt_handler_callback(self, rt_handler_callback_fn):
        if rt_handler_callback_fn is not None:
            self.rt_handler.set_callback_fn(rt_handler_callback_fn)

    def set_quote_handler_callback(self, quote_handler_callback_fn):
        if quote_handler_callback_fn is not None:
            self.quote_handler.set_callback_fn(quote_handler_callback_fn)

    # trade_type: BUY / SELL
    # order_status: FILLED / SUBMITTED
    def get_orders(self, code, trade_side, order_status):
        futu_trade_side = to_futu_trade_side(trade_side)
        status_filter_list = [futu.OrderStatus.FILLED_ALL, futu.OrderStatus.FILLED_PART] \
            if order_status == constants.OrderStatus.FILLED \
            else [futu.OrderStatus.SUBMITTED] if order_status == constants.OrderStatus.SUBMITTED \
            else [futu.OrderStatus.FAILED, futu.OrderStatus.DELETED, futu.OrderStatus.DISABLED,
                  futu.OrderStatus.CANCELLED_ALL, futu.OrderStatus.CANCELLED_PART, futu.OrderStatus.CANCELLING_ALL,
                  futu.OrderStatus.CANCELLING_PART] if order_status == constants.OrderStatus.FAILED \
            else None

        self.get_trade_context().unlock_trade(self.pwd_unlock)
        ret, response = self.get_trade_context().history_order_list_query(code=code,
                                                                          status_filter_list=status_filter_list)
        data = get_data_from_response(code, ret, response)
        if futu_trade_side is not None:
            data = data.loc[(data['trd_side'] == futu_trade_side)]
        results = []
        for index, row_data in data.iterrows():
            order_status = to_order_status(row_data['order_status'])
            trade_side = to_trade_side(row_data['trd_side'])
            results.append((row_data['order_id'], order_status,
                            self.to_timestamp(code, constants.MS_TIME_FORMAT, row_data['create_time']),
                            self.to_timestamp(code, constants.MS_TIME_FORMAT, row_data['updated_time']),
                            trade_side, row_data['price'], int(row_data['qty']),
                            row_data['dealt_avg_price'], int(row_data['dealt_qty'])))
        logging.info("got orders with trade_side({}) and order_status({}) for code {}: filtered number={}"
                     .format(trade_side, status_filter_list, code, len(results)))
        return results

    def get_last_order(self, code, trade_side, order_status_list):
        data = self.get_orders(code, trade_side, order_status_list)
        return get_first_data_from_response(code, futu.RET_OK, data)

    # API doc: https://openapi.futunn.com/futu-api-doc/trade/get-order-list.html
    # return order_status
    def get_order_status_and_price(self, code, order_id):
        ret, response = self.get_trade_context().order_list_query(code=code, order_id=order_id)
        data = get_first_data_from_response(code, ret, response)
        if data is None:
            return None, None
        futu_order_status = data['order_status']
        price = data['dealt_avg_price']
        logging.info(
            "got order status: order_id={}, order_status={}, data={}".format(order_id, futu_order_status, data))
        return to_order_status(futu_order_status), price

    # API doc: https://openapi.futunn.com/futu-api-doc/trade/get-max-trd-qtys.html
    # return pre-trade info (dict with keys: DICT_KEY_MAX_BUY, DICT_KEY_MAX_SELL)
    def get_pre_trade_info(self, code, price):
        ret, response = self.get_trade_context().acctradinginfo_query(futu.OrderType.NORMAL, code, price)
        data = get_first_data_from_response(code, ret, response)
        max_buy = data['max_cash_and_margin_buy']
        max_sell = data['max_position_sell']
        return {constants.DICT_KEY_MAX_BUY: max_buy, constants.DICT_KEY_MAX_SELL: max_sell}

    # API doc: https://openapi.futunn.com/futu-api-doc/trade/place-order.html
    # return order_id
    def place_order(self, code, price, number, order_type, trade_side):
        # precision of stock price should not less than 0.01
        price = round(price, 2)
        futu_trade_side = to_futu_trade_side(trade_side)
        futu_order_type = futu.OrderType.NORMAL if order_type == constants.OrderType.NORMAL else futu.OrderType.MARKET
        ret, response = self.get_trade_context().place_order(price=price, qty=number, code=code,
                                                             order_type=futu_order_type, trd_side=futu_trade_side)
        data = get_first_data_from_response(code, ret, response)
        if data is None:
            msg = "failed to find order id for code {0}".format(code)
            logging.warning(msg)
            raise RuntimeError(msg)
        order_id = data['order_id']
        logging.info('placed order {} for {}: price={}, number={}, order_type={}, trade_side={}'
                     .format(order_id, code, price, number, order_type, trade_side))
        return order_id

    def cancel_order(self, code, order_id):
        ret, data = self.get_trade_context().modify_order(futu.ModifyOrderOp.CANCEL, order_id, 0, 0)
        if ret == futu.RET_ERROR:
            msg = "failed to cancel order {}, ret={}, data={}".format(order_id, ret, data)
            logging.error(msg)
            raise RuntimeError(msg)
        logging.info("canceled order {}: ret={}, data={}".format(order_id, ret, data))

    # API doc: https://openapi.futunn.com/futu-api-doc/quote/get-market-snapshot.html
    # return last price and update time (format: 2021-01-04 16:08:49)
    def get_market_snapshot(self, codes):
        codes = list(codes)
        ret, response = self.get_quote_context().get_market_snapshot(codes)
        data = get_data_from_response(codes, ret, response)
        if data is None:
            msg = "failed to find last price for codes {0}".format(codes)
            logging.info(msg)
            raise RuntimeError(msg)
        result = dict()
        for index, row_data in data.iterrows():
            code = row_data['code']
            last_update_time = row_data['update_time']
            if last_update_time.find('.') != -1:
                last_update_time = last_update_time[:last_update_time.index('.')]
            last_update_timestamp = self.to_timestamp(code, constants.TIME_FORMAT, last_update_time)
            result[code] = (row_data['last_price'], last_update_timestamp, last_update_time)
        return result

    def to_timestamp(self, code, time_format, time):
        code_prefix = code.split('.')[0]
        timezone = self.code_prefix_to_timezone_mapping.get(code_prefix)
        if timezone is None:
            raise RuntimeError(
                "timezone for code prefix {} not found! please give via input code_prefix_to_timezone_mapping".format(
                    code_prefix))
        if timezone != self.local_timezone:
            time = convert_timezone(timezone, self.local_timezone, time_format, time)
        timestamp = time_to_timestamp(time_format, time)
        return timestamp


def get_first_data_from_response(code, ret, data):
    data = get_data_from_response(code, ret, data)
    if len(data) == 0:
        return None
    return data.iloc[0]


def get_data_from_response(code, ret, data):
    if ret == futu.RET_ERROR:
        msg = "failed to request API for code(s) {}, ret={}, data={}".format(code, ret, data)
        raise RuntimeError(msg)
    return data


def to_order_status(futu_order_status):
    return constants.OrderStatus.FILLED if futu_order_status == futu.OrderStatus.FILLED_ALL \
                                           or futu_order_status == futu.OrderStatus.FILLED_PART \
        else constants.OrderStatus.SUBMITTED if (futu_order_status == futu.OrderStatus.SUBMITTED
                                                 or futu_order_status == futu.OrderStatus.WAITING_SUBMIT
                                                 or futu_order_status == futu.OrderStatus.SUBMITTING) \
        else constants.OrderStatus.FAILED


def to_futu_trade_side(trade_side):
    return futu.TrdSide.BUY if trade_side == constants.TradeSide.BUY \
        else futu.TrdSide.SELL if trade_side == constants.TradeSide.SELL \
        else None


def to_trade_side(futu_trade_side):
    return constants.TradeSide.BUY if futu_trade_side == futu.TrdSide.BUY \
        else constants.TradeSide.SELL if futu_trade_side == futu.TrdSide.SELL \
        else None
