from config import *
import sys
import os
import time
import utility as ut
import alpaca_trade_api as tradeapi
import yfinance as yf
from pprint import pprint
import time
import datetime
from datetime import datetime
import pandas as pd
import requests
import json

print('********************* MONITORING SCRIPT ***************************')

api = tradeapi.REST(
        API_KEY,
        SECRET_KEY,
        BASE_URL
    )

stocks_to_check = ['KULR', 'NVDA', 'WISH', 'GME', 'CLOV', 'MVIS', 'BB', 'TLRY', 'MNMD', 'SPY',
                    'RIOT', 'NFLX', 'DKNG', 'SAGE', 'VRM', 'BBBY', 'KOSS', 'AEMD', 'CLNE',
                    'RAD', 'GEO', 'CLF', 'RKT', 'NEXT', 'FAST', 'CRSR', 'JAGX', 'NOK', 'TSLA', 'AMC', 'EXAS']

for x in range (0, len(stocks_to_check)):
    print(stocks_to_check[x])



while True:
    
    for x in range(0,len(stocks_to_check)):
    
        r = requests.get('https://api.polygon.io/v2/aggs/ticker/' + stocks_to_check[x] + '/range/1/minute/2021-06-18/2021-06-18?unadjusted=true&sort=desc&limit=10&apiKey=eVYfnI_fKclE__oNUHZ2iQ_NNCU6I6PlAuoW8E')
        formated_result = r.json()
        most_recent_price = float(formated_result['results'][0]['c'])
        
        price_two_minutes_ago = float(formated_result['results'][2]['c'])
        
        percent_increase = most_recent_price/price_two_minutes_ago
        
        if percent_increase > 1.003:
            print ('Stock Went Up:', stocks_to_check[x])
            print('Percentage Increase: Current Time: ', ut.get_readable_time(formated_result['results'][0]['t']), 'Stock:',  stocks_to_check[x], 'Increased:',  percent_increase)
    
    while True:
        current_time = round(datetime.now().timestamp())
        seconds_in_time = int(current_time % 60)
        
        if seconds_in_time == 5:
            break
        time.sleep(.4)

    

exit()

# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last 5 days'.format(percent_change))