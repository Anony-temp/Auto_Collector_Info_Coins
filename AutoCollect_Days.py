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

def getDayCandle(market_name, to_date, count):
    url = "https://api.upbit.com/v1/candles/days"
    querystring = {"market": market_name, "to": str(to_date)[:19], "count": str(count), "convertingPriceUnit": "KRW"}  # count = # of Candle (Maximum 200)
    response = requests.request("GET", url, params=querystring)
    return response.text

def getDataDay():
    market_codes = json.loads(inquiryMarketCode())
    # print(market_codes)
    count = 1
    if not os.path.exists('CoinData_Days.csv'):
        fp = open('CoinData_Days.csv', 'w')
        fp.write('market, candle_date_time_utc, candle_date_time_kst, opening_price, high_price, low_price, ')
        fp.write('trade_price, timestamp, candle_acc_trade_price, candle_acc_trade_volume, prev_closing_price, ')
        fp.write('change_price, change_rate, converted_trade_price,\n')
        fp.close()
        count = 200
    fp = open('CoinData_Days.csv', 'a')
    for market_code in market_codes:
        # print(market_code)
        time = datetime.now()
        while True:
            day_candles = json.loads(getDayCandle(market_code['market'], time, count))
            print(market_code['market'], time)
            for dc in day_candles:
                if dc['datetime']:
                    fp.write('%s,%s,%s,%g,%g,%g,%g,%d,%g,%g,%g,%g,%g,%g\n' % (dc['market'], dc['candle_date_time_utc'],
                                                               dc['candle_date_time_kst'], dc['opening_price'],
                                                               dc['high_price'], dc['low_price'], dc['trade_price'],
                                                               dc['timestamp'], dc['candle_acc_trade_price'],
                                                               dc['candle_acc_trade_volume'], dc['prev_closing_price'],
                                                               dc['change_price'], dc['change_rate'], dc['converted_trade_price']))
                else:
                    fp.write('%s,%s,%s,%g,%g,%g,%g,None,%g,%g,%g,%g,%g,%g\n' % (dc['market'], dc['candle_date_time_utc'],
                                                                              dc['candle_date_time_kst'],
                                                                              dc['opening_price'],
                                                                              dc['high_price'], dc['low_price'],
                                                                              dc['trade_price'],
                                                                              dc['candle_acc_trade_price'],
                                                                              dc['candle_acc_trade_volume'],
                                                                              dc['prev_closing_price'],
                                                                              dc['change_price'], dc['change_rate'],
                                                                              dc['converted_trade_price']))
            time = time - timedelta(days=count)
            sleep(0.5)
            if count == 1 or time < datetime(2018, 1, 1):
                break
            # sys.exit(1)
    fp.close()

if __name__ == '__main__':
    getDataDay()
