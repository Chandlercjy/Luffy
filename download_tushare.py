import tushare as ts

from awesome_func import handle_error, run_multithreading, show_process


class Tushare(object):

    def __init__(self, path):
        self.start = None  # type: str
        self.code_list = None  # type: list
        self.max_worker = list  # type: int
        self.isindex = False  # type: bool
        self._path = path
        self._finished = []

    @handle_error()
    def _download_df(self, code):
        if self.start:
            dataframe = ts.get_k_data(
                code, start=self.start, index=self.isindex)
        else:
            dataframe = ts.get_k_data(code, index=self.isindex)
        self._save_to_csv(dataframe, code)
        self._show_process()

    def _check(self):
        if self.code_list is None:
            raise Exception("code_list should't be None!")
        print('OK, start to download!')

    def _show_process(self):
        self._finished.append(None)
        show_process(len(self._finished), len(self.code_list))

    def _save_to_csv(self, dataframe, name):
        dataframe.set_index('date', inplace=True)
        dataframe.to_csv(f'{self._path}{name}.csv')

    def download_csv(self):
        self._check()
        run_multithreading(self._download_df,
                           self.code_list, self.max_worker)

    def set_context(self, *args, **kargs):
        for key, value in kargs.items():
            setattr(self, key, value)


if __name__ == "__main__":

    # CODE_LIST = ts.get_hs300s()['code']
    CODE_LIST = ['000001']

    PATH = './what/'
    app = Tushare(PATH)
    app.set_context(code_list=CODE_LIST,
                    start=None,
                    isindex=False,
                    max_worker=500)
    app.download_csv()
