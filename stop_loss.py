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


def change_stop_loss(api, symbol, stop_limit_price):
    
    extended_hours = False

    ut.cancel_all_symbol_orders(api, symbol)
    
    
    current_price = ut.get_current_price_of_stock(symbol)
    
            
    print('********************* Stop Loss ***************************')
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
    print('Average entry price', average_entry_price, 'Starting Position Quantity:', original_position_qty, 'Stop Limt Price:', stop_limit_price)
    
    if float(original_position_qty) < 0:
        print('IS SHORTTTTTTTTTT')
        entry_side = 'sell'
        exit_side = 'buy'
    else:
        print('IS LOOOOOOONNNNGGGGGG')
        entry_side = 'buy'
        exit_side = 'sell'
        
    
    
    result = api.submit_order(
            symbol=symbol,
            qty=abs(original_position_qty),
            side=exit_side,
            type='stop_limit',
            time_in_force='day',
            stop_price=stop_limit_price,
            limit_price=stop_limit_price,
            extended_hours=extended_hours
        )
    
    order_id = result.id
    order_qty = result.qty
    
    buy.protect_from_quick_stop(api, symbol, current_price, stop_limit_price, order_id, average_entry_price, total_order_cost, entry_side, exit_side)



if __name__ == '__main__':
    
    api = tradeapi.REST(
        API_KEY,
        SECRET_KEY,
        BASE_URL
    )
    
    
    symbol = sys.argv[2].upper()
    
    if len(sys.argv) > 3 and sys.argv[3] != 0:
        #This will be a limit buy
        stop_limit_price = float(sys.argv[3])
    else:
        print("Error, need stop_limit price exiting...")
        exit()
    
    change_stop_loss(api, symbol, stop_limit_price)
    
    
    