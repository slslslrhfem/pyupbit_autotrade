import pyupbit
import time
import datetime
import pandas as pd
from tqdm import tqdm
import numpy as np
import statistics
import re


def get_start_time(ticker):
    while True:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
            start_time = df.index[0]
            return start_time
        except:
            pass


# 5분봉 차트 5단위 이동 평균선 조회
def get_ma5(ticker):
    while True:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="minute1", count=5)
            ma20 = df['close'].rolling(5).mean().iloc[-1]
            return ma20
        except:
            pass


# 이전 5분봉 차트 5단위 이동 평균선 조회(하락 판단)
def get_ma5_pre(ticker):
    while True:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="minute1", count=8)
            ma15 = df.head(5)['close'].rolling(5).mean().iloc[-1]
            return ma15
        except:
            pass


# 5분봉 차트 20단위 이동 평균선 조회
def get_ma20(ticker):
    while True:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="minute1", count=20)
            ma20 = df['close'].rolling(20).mean().iloc[-1]
            return ma20
        except:
            pass


# 투자내역 조회
def get_balance(ticker):
    while True:
        try:
            access_key = 'IxNTTErWuBHOhOI2uJ2hSckcYYapNxW1H6Mpnh8p'
            secret_key = 'TwwQFKjABw8AXa6w6iyRC3jOWgUqFbAxfXw2wzCP'
            access = access_key
            secret = secret_key

            upbit = pyupbit.Upbit(access, secret)
            balances = upbit.get_balances()
            print(balances)
            for b in balances:
                if b['currency'] == ticker:
                    if b['balance'] is not None:
                        return float(b['balance'])
                    else:
                        return 0
            return 0
        except:
            pass


# 현재가 조회
def get_current_price(ticker):
    try:
        return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
    except:
        pass


def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def golden_cross_name_finder(ticker_list):
    ticker1 = ticker_list[0][:3]
    print(str(ticker1), "golden_cross list를 불러옵니다..")
    golden_cross_name_list = []
    golden_cross_value_list = []
    values = []
    df_lists = []
    tickers=[]
    for ticker in tqdm(ticker_list):
        while True:
            try:
                df = pd.DataFrame(pyupbit.get_ohlcv(ticker, count=1))
                df_list = np.array(df.values.tolist())
                values.append(df_list[0][5])
                df_lists.append(df_list)
                tickers.append(ticker) #ticker_list와 같긴한데 except고려
                break
            except:
                pass
    min_value = statistics.median(values) * 2
    for i, df_list in enumerate(df_lists):
        while True:
            try:
                ticker = tickers[i]
                if (df_list[0][5] > min_value * 2) and df_list[0][1]>0.00000150: #0.00000150은 btc전용으로, 너무 싼 코인을 안 사게 함. KRW면 바뀔 이유가 있긴 한듯
                    ma5 = get_ma5(ticker)
                    ma20 = get_ma20(ticker)
                    golden_cross_name_list.append(ticker)
                    golden_cross_value_list.append(ma5 / ma20)
                break
            except:
                pass

    return golden_cross_value_list, golden_cross_name_list

def parameter_normalize(parameter,normalizer_num,to_num): # to_num 가까이로 만듬, normalizer_num이 클수록 빠르게 to_num에 가까워진다.
    return_num = (parameter + normalizer_num*to_num)/(normalizer_num+1)
    return return_num

def auto_trader(ticker_list, buy_golden_cross=1.05, sell_parameter=1, sell_golden_cross=1.02):
    buyed_list = []
    selled_list = []
    recent_buyed_list=[]
    buy_num = 0
    # krw_tickers or btc_tickers를 input으로
    access_key = 'IxNTTErWuBHOhOI2uJ2hSckcYYapNxW1H6Mpnh8p'
    secret_key = 'TwwQFKjABw8AXa6w6iyRC3jOWgUqFbAxfXw2wzCP'
    access = access_key
    secret = secret_key

    upbit = pyupbit.Upbit(access, secret)

    while True:
        golden_cross_value_list, golden_cross_name_list = golden_cross_name_finder(ticker_list)
        try:
            index = golden_cross_value_list.index(max(golden_cross_value_list))
        except:
            print("거래대금 50btc 이상의 리스트가 없습니다.")
        print("거래대금 중간값 List는 ", golden_cross_name_list, "입니다.")
        buyed = 0  # test용
        selled = 0  # test용

        while True:
            try:
                recent_buyed_list=[]
                ticker1 = golden_cross_name_list[index][:3]
                ticker2 = golden_cross_name_list[index][4:]
                ticker_to_trade = golden_cross_name_list[index]
                now = datetime.datetime.now()
                start_time = get_start_time(ticker_to_trade)
                end_time = start_time + datetime.timedelta(days=1)
                ma15 = get_ma5(ticker_to_trade)
                ma5_pre = get_ma5_pre(ticker_to_trade)
                ma60 = get_ma20(ticker_to_trade)
                current_price = get_current_price(ticker_to_trade)
                ticker1_balance = get_balance(ticker1)
                ticker2_balance = get_balance(ticker2)
                print("------------------------------------------------------------------------------")
                print("현재 시간 : ", now)
                if len(buyed_list)>1:
                    recent_buyed_list.append(buyed_list[-1][0])
                    recent_buyed_list.append(buyed_list[-2][0])
                elif len(buyed_list)==1:
                    recent_buyed_list.append(buyed_list[-1][0])
                if ma15 / ma60 >= buy_golden_cross:  # 사야하는 상황일때
                    if ticker1 == 'KRW':
                        minimum_balance = 6000
                    else:
                        minimum_balance = 0.0001
                    print("구매하려는 코인은", ticker_to_trade, "입니다.")
                    if ticker1_balance > minimum_balance:
                        print("최소 잔고는 있습니다.")

                    if ticker2 not in recent_buyed_list:
                        print("최근에 이 토큰을 구매한 적이 없습니다.")
                        print("최근에 구매한 코인은", recent_buyed_list, "입니다.")
                    else:
                        print("최근에 이 토큰을 구매한 적이 있습니다.")
                        print("최근에 구매한 코인은", recent_buyed_list, "입니다.")

                    if buyed == 0 and ticker1_balance > minimum_balance and ticker2 not in recent_buyed_list:  # -> krw와 btc의 잔고
                        print("급등 평균선이고, 최근에 매수하지 않았으므로 매수합니다.")

                        upbit.buy_market_order(ticker_to_trade, ticker1_balance * 0.9975)
                        print(str(ticker2), "를", str(current_price), '에 매수했습니다. golden cross rate은 ', str(ma15 / ma60),
                              '입니다.')

                        buyed_list.append((str(ticker2), str(current_price)))
                        buyed = 1

                        time.sleep(5)
                        num = upbit.get_balance(ticker2)
                        orderbook = pyupbit.get_orderbook(ticker_to_trade)
                        all_prices = []
                        for books in orderbook[0]['orderbook_units']:
                            all_prices.append(books['ask_price'])
                            all_prices.append(books['bid_price'])
                        res = all_prices[0]
                        for c in all_prices[1::]:
                            res = gcd(res, c)
                        sell_price = int(int(current_price * 1.06 / res) * res)
                        upbit.sell_limit_order(ticker_to_trade, sell_price, num)  # 이거는 가격 기반 자동 매매까지 해주는 것.


                        buy_num += 1

                        buyed = 1
                    else:
                        if ticker1_balance < minimum_balance:
                            print("씨드가 부족합니다.")
                        if buyed==1:
                            #print("이미 구매한 상태입니다.현재 씨드는",str(ticker1_balance)," 현재 가격은", str(current_price),"BTC golden cross rate은 ", str(ma15 / ma60), '입니다.')
                            #print("현재 수익률은", str(current_price / float(buyed_list[buy_num - 1][1])), "입니다.") # 초회의 경우 list index out of range 이슈가 있음
                            time.sleep(10)
                            num = upbit.get_balance(ticker2)
                            orderbook = pyupbit.get_orderbook(ticker_to_trade)
                            all_prices = []
                            for books in orderbook[0]['orderbook_units']:
                                all_prices.append(books['ask_price'])
                                all_prices.append(books['bid_price'])
                            res = all_prices[0]
                            for c in all_prices[1::]:
                                res = gcd(res, c)
                            sell_price = int(int(current_price * 1.06 /res)*res)
                            upbit.sell_limit_order(ticker_to_trade, sell_price,num)  # 이거는 가격 기반 자동 매매까지 해주는 것.

                            if num>1:
                                selled_price = current_price * 1.08
                            print("이미 구매한 상태로, 매도 가격은 ",selled_price,"에 걸려있습니다.")
                        time.sleep(1)

                    to_sell = get_balance(ticker2)
                    time.sleep(5)
                    if to_sell < minimum_balance:
                        selled_list.append((str(ticker2), str(current_price)))
                        print("아마 본인에의해 판매되었습니다. 최근에 매입/매도되어 구입하지 않은 코인일 수도 있습니다.")
                        break

                else:
                    if buyed == 0:
                        num = upbit.get_balance(ticker2)
                        orderbook = pyupbit.get_orderbook(ticker_to_trade)
                        all_prices = []
                        for books in orderbook[0]['orderbook_units']:
                            all_prices.append(books['ask_price'])
                            all_prices.append(books['bid_price'])
                        res = all_prices[0]
                        for c in all_prices[1::]:
                            res = gcd(res, c)
                        sell_price = int(int(current_price * 1.06 / res) * res)
                        upbit.sell_limit_order(ticker_to_trade, sell_price, num)  # 이거는 가격 기반 자동 매매까지 해주는 것.

                        print("구매한 코인이 없고, 구매할 코인도 없습니다. 다시 이동평균선을 계산합니다. 현재 급등 코인은", str(ticker2), "이고, 현재 가격은",
                              str(current_price), ", 골든크로스 비율은 ", str(ma15 / ma60), "입니다.")
                        print("현재까지", buyed_list, "를 매수했고, ", selled_list, "를 매도했습니다.")
                        print("사용한 parameter은", buy_golden_cross, sell_parameter, sell_golden_cross, "입니다.")
                        final = 1
                        first = 1
                        for coin in buyed_list:
                            first = first * float(coin[1])
                        for coin in selled_list:
                            final = final * float(coin[1])
                        print("총 수익률은, ", str(float(final) / float(first)), "입니다.")
                        filename = str(now) + "results.txt"
                        filename = re.sub("[:/\*?><.]", "", filename)[:11] + str(buy_golden_cross) + str(
                            sell_golden_cross) + str(sell_parameter) + ".txt"
                        f = open(filename, 'w')
                        f.write("현재까지" + str(buyed_list) + "를 매수했고, \n" + str(
                            selled_list) + "를 매도했습니다." + "\n총 수익률은, " + str(final / first) + "입니다.")
                        f.close()
                        time.sleep(1)
                        break
                    to_sell = get_balance(ticker2)
                    if to_sell < 0.001:
                        print("아마 본인에의해 판매되었습니다.")

                        break
                        """
                    if ma15 / ma60 < sell_golden_cross:  # 변수명 ㅈㅅ하지만 ma5나 ma15나 둘다 5개임. sell_parameter가 클수록 쉽게 팜
                        print("15일 이동평균선이 하락하려하여 매도합니다.")
                        upbit.sell_market_order(ticker_to_trade, to_sell*0.997506) # 테스트 중
                        print(str(ticker2), "를", str(current_price), '에', str(to_sell), '만큼 매도했습니다.')
                        selled_list.append((str(ticker2), str(current_price)))
                        break
                    elif ma5_pre * sell_parameter > ma15:
                        print("sell_parameter에 의해 매도합니다.")
                        upbit.sell_market_order(ticker_to_trade, to_sell*0.9975) # 테스트 중
                        print(str(ticker2), "를", str(current_price), '에', str(to_sell), '만큼 매도했습니다.')
                        selled_list.append((str(ticker2), str(current_price)))
                        break
                        """
                    else:
                        print("golden cross는 벗어났습니다. 현재 가격은", str(current_price), "BTC")
                print("보유", str(ticker1), "  : ", str(ticker1_balance), str(ticker1), "/ 보유 ", str(ticker2), " : ",
                      str(ticker2_balance), "/ 골든크로스 비율 : ", str(ma15 / ma60))
                print("현재까지", buyed_list, "를 매수했고, ", selled_list, "를 매도했습니다.")
                print("사용한 parameter은", buy_golden_cross, sell_parameter, sell_golden_cross, "입니다.")

                final = 1
                first = 1
                for coin in buyed_list:
                    first = first * float(coin[1])
                for coin in selled_list:
                    final = final * float(coin[1])
                #print("총 수익률은, ", str(float(final) / float(first)), "입니다.")
                """
                filename = str(now) + "results.txt"
                filename = re.sub("[:/\*?><.]", "", filename)[:11] + str(buy_golden_cross) + str(
                    sell_golden_cross) + str(sell_parameter) + ".txt"
                f = open(filename, 'w')
                f.write("현재까지" + str(buyed_list) + "를 매수했고, \n" + str(selled_list) + "를 매도했습니다." + "\n총 수익률은, " + str(
                    float(final) / float(first)) + "입니다.")
                f.close()
                """
                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)