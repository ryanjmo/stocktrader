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


##change
####   USAGE    ####
#
#python3 buy.py NAME, SYMBOL, FACTOR_OF_MONEY_TO_SPEND, PRICE, STOP_PRICE
#
#####################
    
def protect_from_quick_stop(api, current_price, stop_price, order_id):
    
    try:
        for x in range(0,100000):
        
            ##check to see if price is under and if so sell
            
            if x == 0:
                print('Symbol:', symbol, 'Protecting From A Quick Stop: Average Entry Price', average_entry_price, 'Current Price:', current_price, 'Stop Price', stop_price)
            
            
            if float(current_price) <= float(stop_price):
                time.sleep(1)
                
                cancel_order_info = api.cancel_order(order_id)
                while True:
                    time.sleep(.5)
                    canceled_order_info = api.get_order(cancel_order_info['id'])
                    if canceled_order_info.status == 'pending cancel':
                        'PENDING CANCEL, CONTINUING'
                        continue
                    else:
                        break
             
                quantity_left_to_sell = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
                
                if int(quantity_left_to_sell) == 0:
                    break
                
                result = api.submit_order(
                        symbol=symbol,
                        qty=quantity_left_to_sell,
                        side='sell',
                        type='market',
                        time_in_force='day',
                        extended_hours=extended_hours,
                    )
                
                time.sleep(1)
                
                order_info = api.get_order(resutl['id'])
                
                quantity_left_to_sell = int(order_info.qty) - int(order_info.filled_qty)
                
            if quantity_left_to_buy == 0:
                print("Sold Market... Exiting...")
                
            else:
                print("ERROR, something went wrong, should have sold all. Do a Market Order")
                
                
        
    except KeyboardInterrupt:
        
        all_orders = api.list_orders()
        
        for order in all_orders:
            if order.symbol == symbol:
                api.cancel_order(order.id)
        
        fraction_of_position_to_sell = input('Enter Fraction Of Position You Want Sold: ')
        
        if fraction_of_position_to_sell.isnumeric():
            fraction_of_position_to_sell = int(fraction_of_position_to_sell)
        else:
            fraction_of_position_to_sell = 1
        
        selling_into_strength_input = input('Selling Into Strength. Yes(y) or No(n): ')
       
        if selling_into_strength_input == 'y':
            selling_into_strength = True
        else:
            selling_into_strength = False
        
        sell.sell_the_stock(api, symbol, fraction_of_position_to_sell, extended_hours, selling_into_strength)
    
        
    
if __name__ == '__main__':

    extended_hours = False
        
    api = tradeapi.REST(
            API_KEY,
            SECRET_KEY,
            BASE_URL
        )
        
        
    symbol = sys.argv[2].upper()
    
    all_orders = api.list_orders()
        
    for order in all_orders:
        if order.symbol == symbol:
            api.cancel_order(order.id)
    
    current_price = ut.get_current_price_of_stock(symbol)
    
    
    
    print(current_price)
    
            
    print('********************* BUYING SCRIPT ***************************')
    print('Symbol: ', symbol, ', current_price:', current_price)
    print('')
    
    if len(sys.argv) > 3:
        if sys.argv[3].isnumeric():
            fraction_of_money_to_spend = float(sys.argv[3])
        else:
            print("ERROR... Fraction Of Money To Spend Should Be an Integer")
    else:
        fraction_of_money_to_spend = 4
    
    
    
    
    if len(sys.argv) > 4 and sys.argv[4] != 0:
        #This will be a limit buy
        original_buy_price = float(sys.argv[4])
        factor_over_price_accepted = 1.00025
        stop_out_factor = .998
        limit_buy = True
        
    else:
        #This will be a market buy
        original_buy_price = current_price
        factor_over_price_accepted = 1.001
        stop_out_factor = .998
        limit_buy = False
        
        
        
    
    if len(sys.argv) > 5:
        entered_stop_price = True
        stop_price  = float(sys.argv[5])
        
    else:
        entered_stop_price = False
        stop_price = float(original_buy_price)*stop_out_factor
        
    
        
    #limit_price_for_stop = stop_price*.998
    limit_price_for_stop = stop_price*1
    
    
    
    max_buy_price = ut.round_to_two((original_buy_price)*factor_over_price_accepted)
    
    print('Buying Program Started...')
    original_position = ut.get_symbol_position(api, symbol)
    if original_position == 0:
        original_symbol_quantity = 0;
    else:
        original_symbol_quantity = original_position.qty
    print('Starting Position Quantity:', original_symbol_quantity)
    print('Target Buy Price:', original_buy_price)
    print('Maximum Buy Price', max_buy_price)
    print('Stop Factor:', stop_out_factor)
    print('Estimated Stop Out Price', ut.round_to_two(stop_price))
    print('Limit Price', ut.round_to_two(limit_price_for_stop))
    
    
    account = api.get_account()
    
    print('Account Total Portfolio Value: ', account.portfolio_value)
    
    
    account_portfolio_value = int(float(account.portfolio_value))
    
    original_quantity_to_buy = (float(account_portfolio_value)/fraction_of_money_to_spend)/float(max_buy_price)
    
    if fraction_of_money_to_spend == 1:
        original_quantity_to_buy -= 1
    
    
    original_quantity_to_buy = int(original_quantity_to_buy)
    print('Quantity of ', symbol ,' Trying To Buy: ', int(original_quantity_to_buy))
    print('Maximum Cost of Order: ', ut.round_to_two((original_quantity_to_buy) * float(max_buy_price)))
    print('')
    
    
    result = api.submit_order(
        symbol=symbol,
        qty=original_quantity_to_buy,
        side='buy',
        type='limit',
        time_in_force='day',
        limit_price=max_buy_price,
        extended_hours=extended_hours,
        order_class='oto',
        stop_loss={'stop_price': original_buy_price*stop_out_factor,
                   'limit_price':  original_buy_price*stop_out_factor}
        )
    
    
    order_id = result.id
    order_qty = result.qty
    
    for x in range(0,100000):
        
        time.sleep(.5)
        
        current_order_info = api.get_order(order_id)
        quantity_left_to_buy = int(current_order_info.qty) - int(current_order_info.filled_qty)
        current_price = ut.get_current_price_of_stock(symbol)
        
        if x%10 == 0:
            
            print("Symbol", symbol, "Quantity Left To Buy", quantity_left_to_buy, "Quantity filled:", order_id.filled_qty, "Quantity started:", order_qty.qty)
            print("Current Price", current_price, "Quantity Left To Buy:", quantity_left_to_buy, "At Price", max_buy_price)
        
        
        current_order_info = api.get_order(current_order_info['id'])
        quantity_left_to_buy = int(current_order_info.qty) - int(current_order_info.filled_qty)
        if quantity_left_to_buy == 0:
            print("Buying Complete, going to check stop loss.")
            
        order_id = current_order_info['id']
    
    
    current_symbol_position = ut.get_symbol_position(api, symbol)
    average_entry_price = float(current_symbol_position.avg_entry_price)
    current_position_qty = int(current_symbol_position.qty)
    
        
    
    if entered_stop_price == False:
        stop_price = average_entry_price*stop_out_factor
        
    current_price = ut.get_current_price_of_stock(symbol)
    
    if current_price <= stop_price:
        stop_price = ut.round_to_two(current_price*.9997)
        if float(stop_price) == float(math.floor(current_price * 100)/100.0):
            stop_price = float(stop_price) - .01
        
    
    protect_from_quick_stop(api, current_price, stop_price, order_id)
    