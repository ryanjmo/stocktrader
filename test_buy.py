import sys
if sys.argv[1] == 'ryan':
    from config import *
if sys.argv[1] == 'chrissy':
    from config_chrissy import *
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
import sell_7_seconds as sell
import math
import buy


##change
####   USAGE    ####
#
#python3 buy.py NAME, SYMBOL, FACTOR_OF_MONEY_TO_SPEND, PRICE, STOP_PRICE
#
#####################


api = tradeapi.REST(
        API_KEY,
        SECRET_KEY,
        BASE_URL
    )
    
    
symbol = sys.argv[2].upper()

extended_hours = False

ut.cancel_all_symbol_orders(api, symbol)

current_price = ut.get_current_price_of_stock(symbol)
    
            
print('********************* Enter After Hours ***************************')
print('Symbol: ', symbol, ', current_price:', current_price)
print('')


if sys.argv[1] == 'ryan':
    account_portfolio_value = 100
if sys.argv[1] == 'chrissy':
    account_portfolio_value = 100
    
original_quantity_to_buy = int(float(account_portfolio_value)/float(current_price))

limit_price = float(current_price)*1.01

result = api.submit_order(
    symbol=symbol,
    qty=1,
    side='buy',
    type='market',
    time_in_force='day',
    extended_hours=extended_hours
)

result = api.submit_order(
    symbol=symbol,
    qty=1,
    side='sell',
    type='limit',
    limit_price=limit_price,
    time_in_force='day',
    extended_hours=extended_hours
)

result = api.submit_order(
    symbol=symbol,
    qty=1,
    side='sell',
    type='limit',
    limit_price=limit_price,
    time_in_force='day',
    extended_hours=extended_hours
)



