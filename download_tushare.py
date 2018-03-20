import tushare as ts
from retry import retry

from awesome_func import run_multithreading, show_process

PATH = './what/'
INDEX_LIST = []
START = None
FINISHED = []


@retry(tries=20)
def download_ohlc(index):
    try:
        if START:
            df = ts.get_k_data(index, start=START)
        else:
            df = ts.get_k_data(index)
        df.to_csv(f'{path}{index}.csv')
        FINISHED.append(index)
        show_process(len(FINISHED), len(INDEX_LIST))
    except Exception as error:
        print(f'Raise an error: {error}')
        print(f'Start to retry!!!!!')
        raise Exception




if __name__ == "__main__":

    INDEX_LIST = ts.get_hs300s()['code']

    run_multithreading(download_ohlc, INDEX_LIST, 500)
