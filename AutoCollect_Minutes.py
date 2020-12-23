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

def getMinuteCandle(market_name):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": market_name, "count": "200"}  # count = # of Candle (Maximum 200)
    response = requests.request("GET", url, params=querystring)
    return response.text

def getDataMinute():
    market_codes = json.loads(inquiryMarketCode())
    # print(market_codes)
    if not os.path.exists('CoinData_Minutes.csv'):
        fp = open('CoinData_Minutes.csv', 'w')
        fp.write('market, candle_date_time_utc, candle_date_time_kst, opening_price, high_price, low_price, ')
        fp.write('trade_price, timestamp, candle_acc_trade_price, candle_acc_trade_volume,\n')
        fp.close()
    while True:
        fp = open('CoinData_Minutes.csv', 'a')
        now_time = datetime.now()
        for market_code in market_codes:
            # print(market_code)
            minute_candles = json.loads(getMinuteCandle(market_code['market']))
            print(market_code['market'], datetime.now())
            for mc in minute_candles:
                fp.write('%s,%s,%s,%g,%g,%g,%g,%d,%g,%g,\n' % (mc['market'], mc['candle_date_time_utc'],
                                                               mc['candle_date_time_kst'], mc['opening_price'],
                                                               mc['high_price'], mc['low_price'], mc['trade_price'],
                                                               mc['timestamp'], mc['candle_acc_trade_price'],
                                                               mc['candle_acc_trade_volume']))
            # sys.exit(1)
            sleep(0.5)
        fp.close()
        while True:
            if datetime.now() > now_time + timedelta(minutes=99, seconds=30):
                break
            sleep(0.5)
        # sleep(200)

if __name__ == '__main__':
    getDataMinute()
