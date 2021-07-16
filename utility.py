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

def get_symbol_position(api, symbol):
    try:
        position = api.get_position( symbol)
        return position
    
    except Exception as e:
        is_error = True
        ut.print_error(e)
        return 0
        
        
def print_error(e):
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    
def round_to_two(number):
    return str(round(number, 2))


def get_readable_time(time_to_get):
    
    if len(str(time_to_get)) > 10:
        time_to_get = int(int(time_to_get)/1000.0)
        
    time_to_get += 60*60*2
    
    date = datetime.datetime.fromtimestamp(time_to_get).strftime('%Y-%m-%d')
    
    if date > '2022-11-03':
        time_to_get = time_to_get - 7*60*60
    elif date > '2022-03-10':
        time_to_get = time_to_get - 6*60*60
    elif date > '2021-11-03':
        time_to_get = time_to_get - 7*60*60
    elif date > '2021-03-10':
        time_to_get = time_to_get - 6*60*60
    elif date > '2020-11-03':
        time_to_get = time_to_get - 7*60*60
    elif date > '2020-3-10':
        time_to_get = time_to_get - 6*60*60
    elif date > '2019-11-03':
        time_to_get = time_to_get - 7*60*60
    elif date > '2019-03-10':
        time_to_get = time_to_get - 6*60*60
    elif date > '2018-11-04':
        time_to_get = time_to_get - 7*60*60
    elif date > '2018-03-11':
        time_to_get = time_to_get - 6*60*60
    elif date > '2017-11-05':
        time_to_get = time_to_get - 7*60*60
    elif date > '2017-03-12':
        time_to_get = time_to_get - 6*60*60
    else:
        time_to_get = time_to_get - 7*60*60

    
    return datetime.datetime.fromtimestamp(time_to_get).strftime('%Y-%m-%d %H:%M:%S')
    
    
def cancel_order_and_calculate_quanity_left_to_sell(api, order_info):
    
    cancel_order_info = api.cancel_order(order_info['id'])
    canceled_order_info = api.get_order(order_info['id'])
    print(canceled_order_info)
    print("Quantity filled:", canceled_order_info.filled_qty)
    print("Quantity started:", canceled_order_info.qty)
    quantity_left_to_sell = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
    print("Quantity Left To Sell:", quantity_left_to_sell)
    return quantity_left_to_sell
    
def get_current_price_of_stock(symbol):
    r = requests.get('https://api.polygon.io/v2/last/trade/' + symbol + '?&apiKey=eVYfnI_fKclE__oNUHZ2iQ_NNCU6I6PlAuoW8E')
    formated_result = r.json()
    return float(formated_result['results']['p'])
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def cancel_all_symbol_orders(api, symbol):
    
    all_orders = api.list_orders()
        
    for order in all_orders:
        if order.symbol == symbol:
            api.cancel_order(order.id)
    