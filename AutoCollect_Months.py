import os
from time import sleep
import json
import requests
from datetime import datetime, timedelta

def inquiryMarketCode():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "false"}
    response = requests.request("GET", url, params=querystring)
    return response.text

def getMonthCandle(market_name, to_date, count):
    url = "https://api.upbit.com/v1/candles/months"
    querystring = {"market": market_name, "to": str(to_date)[:19], "count": str(count)}  # count = # of Candle (Maximum 200)
    response = requests.request("GET", url, params=querystring)
    return response.text

def getDataMonth():
    market_codes = json.loads(inquiryMarketCode())
    # print(market_codes)
    count = 1
    if not os.path.exists('CoinData_Months.csv'):
        fp = open('CoinData_Months.csv', 'w')
        fp.write('market, candle_date_time_utc, candle_date_time_kst, high_price, low_price, ')
        fp.write('trade_price, timestamp, candle_acc_trade_price, candle_acc_trade_volume, first_day_of_period\n')
        fp.close()
        count = 12
    fp = open('CoinData_Months.csv', 'a')
    for market_code in market_codes:
        # print(market_code)
        time = datetime.now()
        while True:
            month_candles = json.loads(getMonthCandle(market_code['market'], time, count))
            print(market_code['market'], time)
            for mc in month_candles:
                if mc['timestamp']:
                    fp.write('%s,%s,%s,%g,%g,%g,%g,%d,%g,%g,%s\n' % (mc['market'], mc['candle_date_time_utc'],
                                                               mc['candle_date_time_kst'], mc['opening_price'],
                                                               mc['high_price'], mc['low_price'], mc['trade_price'],
                                                               mc['timestamp'], mc['candle_acc_trade_price'],
                                                               mc['candle_acc_trade_volume'], mc['first_day_of_period']))
                else:
                    fp.write('%s,%s,%s,%g,%g,%g,%g,None,%g,%g,%s\n' % (mc['market'], mc['candle_date_time_utc'],
                                                             mc['candle_date_time_kst'], mc['opening_price'],
                                                             mc['high_price'], mc['low_price'], mc['trade_price'],
                                                             mc['candle_acc_trade_price'], mc['candle_acc_trade_volume'],
                                                             mc['first_day_of_period']))
            time = time - timedelta(days=365)
            if count == 1 or time < datetime(2018, 1, 1):
                break
            sleep(0.5)
        # sys.exit(1)
    fp.close()

if __name__ == '__main__':
    getDataMonth()
