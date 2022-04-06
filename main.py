from pyupbit_util import *
import pyupbit_util_realtrade
import multiprocessing
import numpy as np

if __name__ == '__main__':
    access_key = 'IxNTTErWuBHOhOI2uJ2hSckcYYapNxW1H6Mpnh8p'
    secret_key = 'TwwQFKjABw8AXa6w6iyRC3jOWgUqFbAxfXw2wzCP'
    server_url = 'https://api.upbit.com'

    access = access_key
    secret = secret_key

    upbit = pyupbit.Upbit(access, secret)
    print("Login Success")


    #upbit.sell_limit_order('BTC-HUNT', num)
    tickers = pyupbit.get_tickers()
    krw_tickers=[]
    btc_tickers=[]
    buy_gold_list=[1.03,1.04,1.05] #이거는 1.05가 best tuning같긴 함. 그런데 1.07도 완전 급등만 잡긴 하지만 괜찮을수도?
    sell_gold_list=[0.5] # 이거는 아직 모름. 낮을수록 늦게팜 1.0수준이면 거의 안파는 수준 ->20과 5를 봐서 비율 1.03느낌
    sell_parameter_list=[0.5] # 이거는 갠적으로 1과 1.05 사이 무언가 정도면 괜찮은듯. 1.05는 너무 빠름. 경우에따라 오르다가 팔기도 함 ->8분~3분전을 봐서 5분~0분과 비율 느낌
    multiprocessing_arguments=[]

    for ticker in tickers:
        if ticker[0]=='K':
            krw_tickers.append(ticker)
        elif ticker[0]=='B':
            btc_tickers.append(ticker)

    ticker_arg=[(btc_tickers,1.05,123,123)]#, (btc_tickers,1.05,123,123)] # 123은 의미 없다

    for arg in ticker_arg:
        proc = multiprocessing.Process(target=pyupbit_util_realtrade.auto_trader,args=arg)
        multiprocessing_arguments.append(proc)
        proc.start()
    for proc in multiprocessing_arguments:
        proc.join()


    """
    for goldbuyes in buy_gold_list:
        for goldselles in sell_gold_list:
            for sell_params in sell_parameter_list:
                proc= multiprocessing.Process(target=auto_trader,args=(btc_tickers, goldbuyes,goldselles, sell_params))
                multiprocessing_arguments.append(proc)
                proc.start()
    for proc in multiprocessing_arguments:
        proc.join()
    """


    #auto_trader(btc_tickers,1.05,1.02,1.01) # Default, Test

    #pyupbit_util_realtrade.auto_trader(btc_tickers,1.05,1.02,1.01) # 진짜 돈으로 와리가리 함(아마)
