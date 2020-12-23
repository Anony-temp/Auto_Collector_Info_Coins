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

def getWeekCandle(market_name, to_date, count):
    url = "https://api.upbit.com/v1/candles/weeks"
    querystring = {"market": market_name, "to": str(to_date)[:19], "count": str(count)}  # count = # of Candle (Maximum 200)
    response = requests.request("GET", url, params=querystring)
    return response.text

def getDataWeek():
    market_codes = json.loads(inquiryMarketCode())
    # print(market_codes)
    count = 1
    if not os.path.exists('CoinData_Weeks.csv'):
        fp = open('CoinData_Weeks.csv', 'w')
        fp.write('market, candle_date_time_utc, candle_date_time_kst, high_price, low_price, ')
        fp.write('trade_price, timestamp, candle_acc_trade_price, candle_acc_trade_volume, first_day_of_period\n')
        fp.close()
        count = 50
    fp = open('CoinData_Weeks.csv', 'a')
    for market_code in market_codes:
        # print(market_code)
        time = datetime.now()
        while True:
            week_candles = json.loads(getWeekCandle(market_code['market'], time, count))
            print(market_code['market'], time)
            for wc in week_candles:
                if wc['timestamp']:
                    fp.write('%s,%s,%s,%g,%g,%g,%g,%d,%g,%g,%s\n' % (wc['market'], wc['candle_date_time_utc'],
                                                               wc['candle_date_time_kst'], wc['opening_price'],
                                                               wc['high_price'], wc['low_price'], wc['trade_price'],
                                                               wc['timestamp'], wc['candle_acc_trade_price'],
                                                               wc['candle_acc_trade_volume'], wc['first_day_of_period']))
                else:
                    fp.write('%s,%s,%s,%g,%g,%g,%g,None,%g,%g,%s\n' % (wc['market'], wc['candle_date_time_utc'],
                                                                     wc['candle_date_time_kst'], wc['opening_price'],
                                                                     wc['high_price'], wc['low_price'],
                                                                     wc['trade_price'],
                                                                     wc['candle_acc_trade_price'],
                                                                     wc['candle_acc_trade_volume'],
                                                                     wc['first_day_of_period']))
            time = time - timedelta(weeks=50)
            if count == 1 or time < datetime(2018, 1, 1):
                break
            sleep(0.5)
        # sys.exit(1)
    fp.close()

if __name__ == '__main__':
    getDataWeek()
