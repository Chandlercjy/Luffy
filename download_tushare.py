from functools import wraps

import tushare as ts
from retry import retry

from awesome_func import handle_error, run_multithreading, show_process


class Tushare(object):

    def __init__(self, path):
        self.start = None
        self.index_list = None
        self.max_worker = 500
        self._path = path
        self._finished = []

    @handle_error()
    def download_ohlc(self, index):
        if self.start:
            df = ts.get_k_data(index, start=self.start)
        else:
            df = ts.get_k_data(index)
        df.to_csv(f'{self._path}{index}.csv')
        self._finished.append(index)
        show_process(len(self._finished), len(self.index_list))

    def download_csv(self):
        self._check()
        run_multithreading(self.download_ohlc,
                           self.index_list, self.max_worker)

    def _check(self):
        if self.index_list is None:
            raise Exception("index_list should't be None!")
        print('OK, start to download!')



if __name__ == "__main__":
    # INDEX_LIST = ts.get_hs300s()['code']
    INDEX_LIST = ['000001', '000002']
    # run_multithreading(download_ohlc, INDEX_LIST, 500)

    PATH = './what/'
    app = Tushare(PATH)
    app.index_list = None
    app.start = None
    app.max_worker = 500
    app.download_csv()
