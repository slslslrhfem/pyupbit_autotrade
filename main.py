from pyupbit_util import *
import pyupbit_util_realtrade
import multiprocessing
import numpy as np

if __name__ == '__main__':
    access_key = "Your Access Key"
    secret_key = "Your Secret Key"
    server_url = 'https://api.upbit.com'

    access = access_key
    secret = secret_key

    upbit = pyupbit.Upbit(access, secret)
    print("Login Success")


    #upbit.sell_limit_order('BTC-HUNT', num)
    tickers = pyupbit.get_tickers()
    krw_tickers=[]
    btc_tickers=[]
    buy_gold_list=[1.03,1.04,1.05] 
    sell_gold_list=[0.5] 
    sell_parameter_list=[0.5] 
    multiprocessing_arguments=[]

    for ticker in tickers:
        if ticker[0]=='K':
            krw_tickers.append(ticker)
        elif ticker[0]=='B':
            btc_tickers.append(ticker)

    ticker_arg=[(btc_tickers,1.05,123,123)]#, (btc_tickers,1.05,123,123)] # 123은 의미 없다. 매수만 하도록 구현이 되어있기 때문
    
    auto_trader(btc_tickers,1.05,1.02,1.01) # Default, Test
    """
    for arg in ticker_arg:
        proc = multiprocessing.Process(target=pyupbit_util_realtrade.auto_trader,args=arg)
        multiprocessing_arguments.append(proc)
        proc.start()
    for proc in multiprocessing_arguments:
        proc.join()
    """

    """
    for goldbuyes in buy_gold_list:
        for goldselles in sell_gold_list:
            for sell_params in sell_parameter_list:
                proc= multiprocessing.Process(target=auto_trader,args=(btc_tickers, goldbuyes,goldselles, sell_params)) #Parameter 시험용
                multiprocessing_arguments.append(proc)
                proc.start()
    for proc in multiprocessing_arguments:
        proc.join()
    """


    #pyupbit_util_realtrade.auto_trader(btc_tickers,1.05,1.02,1.01) # 진짜 돈으로 와리가리 함
