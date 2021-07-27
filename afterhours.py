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

extended_hours = True

ut.cancel_all_symbol_orders(api, symbol)

current_price = ut.get_current_price_of_stock(symbol)
    
            
print('********************* After Hours ***************************')
print('Symbol: ', symbol, ', current_price:', current_price)
print('')

original_symbol_position = ut.get_symbol_position(api, symbol)
        
print("Original Symbol Position:", original_symbol_position)
if original_symbol_position == 0:
    print("No Symbol Position.. Exiting...")
    exit()
original_position_qty = int(original_symbol_position.qty)

average_entry_price = float(original_symbol_position.avg_entry_price) 
total_order_cost = original_position_qty*average_entry_price
print('Average entry price', average_entry_price, 'Starting Position Quantity:', original_position_qty)

limit_price = float(current_price)*.99

result = api.submit_order(
    symbol=symbol,
    qty=abs(original_position_qty),
    side='sell',
    type='limit',
    limit_price=limit_price,
    time_in_force='day',
    extended_hours=extended_hours
)

