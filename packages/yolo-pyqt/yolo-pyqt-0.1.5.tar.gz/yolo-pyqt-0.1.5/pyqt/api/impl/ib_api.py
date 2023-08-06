import math
import ib_insync
from pyqt.api import interface, constants
from pyqt.utils.time import *
import concurrent
import asyncio
import logging
from apscheduler.schedulers import background


class IbAPI(interface.API):

    def __init__(self, host, port, client_id, exchange='SMART', currency='USD',
                 check_connection_interval_s=60, refresh_interval_s=1):
        self.__ib_client = IbClient(host, port, client_id, exchange, currency)
        self.__scheduler = background.BackgroundScheduler()
        self.__check_connection_interval_s = check_connection_interval_s
        self.__refresh_interval_s = refresh_interval_s
        # 0 - running flag, 1 - IB connection
        self.__check_job_id = "keep_ib_conn"
        self.__refresh_job_id = "refresh_tickers"
        # the number of thread must be 1 since asyncio only support operations in a single thread!
        self.__executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def start(self):
        # start scheduler
        self.__scheduler.start()
        # start ib connection
        self.check_ib_client_connected()
        # periodically check to keep connection
        self.__scheduler.add_job(self.check_ib_client_connected, trigger='interval',
                                 seconds=self.__check_connection_interval_s, id=self.__check_job_id)
        self.__scheduler.add_job(self.refresh_tickers, trigger='interval',
                                 seconds=self.__refresh_interval_s, id=self.__refresh_job_id)
        logging.info("add periodical jobs: {}".format([self.__check_job_id, self.__refresh_job_id]))

    def check_ib_client_connected(self):
        return self.execute_ib_task(self.__ib_client.check_connected, None, error_result=None)

    def execute_ib_task(self, fn, args, error_result):
        if args is None:
            task = self.__executor.submit(fn)
        else:
            task = self.__executor.submit(fn, *args)
        try:
            return task.result()
        except Exception as ex:
            logging.error("failed to execute ib task: {}".format(str(ex)), None)
            return error_result

    def stop(self):
        self.__ib_client.stop()

    def get_market_snapshot(self, codes):
        return self.execute_ib_task(self.__ib_client.get_market_snapshot, [codes], error_result=dict())

    def get_pre_trade_info(self, code, price):
        return self.execute_ib_task(self.__ib_client.get_pre_trade_info, [code, price],
                                    error_result={constants.DICT_KEY_MAX_BUY: 0, constants.DICT_KEY_MAX_SELL: 0})

    def get_orders(self, code, trade_side, order_status):
        return self.execute_ib_task(self.__ib_client.get_orders, [code, trade_side, order_status],
                                    error_result=list())

    def get_order_status_and_price(self, code, order_id):
        return self.execute_ib_task(self.__ib_client.get_order_status_and_price, [code, order_id],
                                    error_result=(None, None))

    def place_order(self, code, price, number, order_type, trade_side):
        return self.execute_ib_task(self.__ib_client.place_order, [code, price, number, order_type, trade_side],
                                    error_result=None)

    def cancel_order(self, code, order_id):
        return self.execute_ib_task(self.__ib_client.cancel_order, [code, order_id], error_result=False)

    def refresh_tickers(self):
        return self.execute_ib_task(self.__ib_client.refresh, None, error_result=None)


# all functions should be executed in the same thread!!!
class IbClient:

    def __init__(self, host, port, client_id, exchange, currency):
        self.__host = host
        self.__port = port
        self.__client_id = client_id
        self.__exchange = exchange
        self.__currency = currency
        self.__ib = None
        # key fields for API to communicate with IB connection
        self.__subscribed_codes = set()
        self.__tickers = dict()
        self.__running = True

    def check_connected(self):
        if not self.__running:
            return
        # required in non-main thread
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            logging.info("set event loop: {}".format(event_loop))
        if self.__ib is not None:
            try:
                open_orders = self.__ib.reqAllOpenOrders()
                logging.info("successfully checked ib connection with {} open orders".format(len(open_orders)))
                return
            except Exception as ex:
                logging.error("failed to check ib connection", ex)
        logging.info("restart ib connection...")
        self.__start_ib_conn()

    def refresh(self):
        self.__ib.sleep(0.1)

    def stop(self):
        if self.__ib is not None:
            self.__ib.disconnect()
        self.__running = False

    def __start_ib_conn(self):
        self.__subscribed_codes = set()
        self.__tickers = dict()
        # established ib connection
        self.__ib = ib_insync.IB()
        try:
            self.__ib.connect(self.__host, self.__port, self.__client_id)
            logging.info("successfully established ib connection!")
        except Exception as ex:
            logging.error("failed to connect to IB API server", ex)

    def get_market_snapshot(self, codes):
        """
        :param codes: set type, tells which stocks or coins are required
        :return: map<code, tuple(last_price, update_timestamp, update_local_time)>
            update_local_time format: %Y-%m-%d %H:%M:%S
        """
        results = dict()
        if self.__ib is None:
            return results
        for code in codes:
            normalized_code = normalize_code(code)
            ticker = self.__tickers.get(normalized_code)
            if ticker is None:
                if normalized_code not in self.__subscribed_codes:
                    stock = ib_insync.Stock(normalized_code, self.__exchange, self.__currency)
                    ticker = self.__ib.reqMktData(stock, snapshot=False)
                    logging.info("subscribed new code {} as {}".format(code, normalized_code))
                    self.__tickers[normalized_code] = ticker
                    self.__subscribed_codes.add(normalized_code)
                continue
            stock_data = get_stock_data(ticker)
            if stock_data is not None:
                results[code] = stock_data
        return results

    # get_pre_trade_info is used for checking before submitting an order,
    # we need to know how many stocks or coins at most we can buy or sell.
    # return pre-trade info (dict with keys: DICT_KEY_MAX_BUY, DICT_KEY_MAX_SELL)
    def get_pre_trade_info(self, code, price):
        if self.__ib is None:
            return {constants.DICT_KEY_MAX_BUY: 0, constants.DICT_KEY_MAX_SELL: 0}
        # get max_sell from position
        normalized_code = normalize_code(code)
        positions = self.__ib.positions()
        max_sell = 0
        for position in positions:
            if position.contract.symbol != normalized_code:
                continue
            max_sell = position.position
            break
        # get max_buy from account summary
        account_values = self.__ib.accountSummary()
        cash_value = 0
        for acc_value in account_values:
            if acc_value.tag == 'TotalCashValue':
                cash_value = float(acc_value.value)
        return {constants.DICT_KEY_MAX_BUY: cash_value/price, constants.DICT_KEY_MAX_SELL: max_sell}

    # trade_type: BUY / SELL
    # order_status: SUBMITTED / FILLED / FAILED
    def get_orders(self, code, trade_side, order_status):
        """
        :return: order list by order ID in descending order
            [<order X>, <order X-1>, ...]
            order format: (order_id, status, create_timestamp, update_timestamp, trade_side,
                            submit_price, submit_num, filled_avg_price, filled_num)
        """
        if self.__ib is None:
            return list()
        expected_query_fn = self.__ib.trades
        if order_status == constants.OrderStatus.SUBMITTED:
            expected_status_set = ib_insync.OrderStatus.ActiveStates
        elif order_status == constants.OrderStatus.FILLED:
            expected_status_set = {ib_insync.OrderStatus.Filled}
        elif order_status == constants.OrderStatus.FAILED:
            expected_status_set = {ib_insync.OrderStatus.Inactive, ib_insync.OrderStatus.Cancelled,
                                   ib_insync.OrderStatus.ApiCancelled}
        trades = expected_query_fn()
        results = list()
        normalized_code = normalize_code(code)
        for trade in trades:
            if normalized_code != trade.contract.symbol:
                continue
            if trade_side is not None and trade_side.name != trade.order.action:
                continue
            if trade.orderStatus.status not in expected_status_set:
                continue
            results.append(convert_trade_to_api_order(trade))
        return results

    # get status and avg price for specified order
    def get_order_status_and_price(self, code, order_id):
        """
        :return: (order_status, price) (tuple)
        """
        if self.__ib is None:
            return None, None
        normalized_code = normalize_code(code)
        for trade in self.__ib.trades():
            if trade.contract.symbol != normalized_code:
                continue
            if trade.order.orderId != order_id:
                continue
            return to_order_status(trade.orderStatus.status), trade.orderStatus.avgFillPrice

    # place order for specified code
    def place_order(self, code, price, number, order_type, trade_side):
        """
        :return: new_order_id
        """
        if self.__ib is None:
            return None
        ib_trade_side = 'BUY' if trade_side == constants.TradeSide.BUY \
            else 'SELL' if trade_side == constants.TradeSide.SELL \
            else None
        if ib_trade_side is None:
            return None
        if order_type == constants.OrderType.NORMAL:
            price = round(price, 2)
            order = ib_insync.LimitOrder(ib_trade_side, number, price)
            # allow trade in pre-market or post-market time
            order.outsideRth = True
        else:
            order = ib_insync.MarketOrder(ib_trade_side, number)
        contract = ib_insync.Stock(normalize_code(code), self.__exchange, self.__currency)
        trade = self.__ib.placeOrder(contract, order)
        return trade.order.orderId

    def cancel_order(self, code, order_id):
        """
        :return: is_succeed (bool)
        """
        if self.__ib is None:
            return False
        selected_order = None
        for open_order in self.__ib.orders():
            if open_order.orderId == order_id:
                selected_order = open_order
        if selected_order is None:
            # already canceled
            return True
        self.__ib.cancelOrder(selected_order)
        return True


def convert_trade_to_api_order(trade):
    """
    order format: (order_id, status, create_timestamp, update_timestamp, trade_side,
                        submit_price, submit_num, filled_avg_price, filled_num)
    """
    create_timestamp, update_timestamp = 0, 0
    if trade.log:
        create_timestamp = trade.log[0].time.timestamp()
        update_timestamp = trade.log[len(trade.log)-1].time.timestamp()
    trade_side = constants.TradeSide.BUY if trade.order.action == 'BUY' else constants.TradeSide.SELL
    submit_price = trade.order.lmtPrice if trade.order.orderType == 'LMT' else None
    submit_num = trade.order.totalQuantity
    filled_avg_price = trade.orderStatus.avgFillPrice
    filled_num = trade.orderStatus.filled
    return (trade.order.orderId, trade.orderStatus.status, create_timestamp, update_timestamp,
            trade_side, submit_price, submit_num, filled_avg_price, filled_num)


def to_order_status(ib_order_status):
    if ib_order_status in ib_insync.OrderStatus.ActiveStates:
        return constants.OrderStatus.SUBMITTED
    elif ib_order_status == ib_insync.OrderStatus.Filled:
        return constants.OrderStatus.FILLED
    else:
        return constants.OrderStatus.FAILED


def get_stock_data(ticker):
    last_price = ticker.last if math.isnan(ticker.last) else ticker.midpoint()
    if math.isnan(last_price):
        return None
    last_update_timestamp = ticker.time.timestamp()
    last_update_time = timestamp_to_time(constants.TIME_FORMAT, last_update_timestamp)
    return last_price, last_update_timestamp, last_update_time


def normalize_code(code):
    return code.split('.')[1] if code.find('.') > 0 else code
