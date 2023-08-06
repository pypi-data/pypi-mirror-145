from pyqt.api.impl.ib_api import IbAPI
import time
import unittest


class TestIbAPI(unittest.TestCase):

    def setUp(self):
        self.__ib_api = IbAPI('127.0.0.1', 7496, 526)
        self.__ib_api.start()

    def test_market_snapshot(self):
        while True:
            start = time.time()
            data = self.__ib_api.get_market_snapshot(['AAPL', 'TSLA'])
            print('data=', data, 'time=', time.time()-start)
            time.sleep(1)
