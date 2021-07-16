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
import stop_loss as stop


##change
####   USAGE    ####
#
#python3 buy.py NAME, SYMBOL, FACTOR_OF_MONEY_TO_SPEND, PRICE, STOP_PRICE
#
#####################
    
def protect_from_quick_stop(api, symbol, current_price, stop_price, order_id, average_entry_price, total_order_cost):
    
    stop_price = float(stop_price)
    
    extended_hours = False
    
    try:
        for x in range(0,100000):
        
            ##check to see if price is under and if so sell
            
            if x%50 == 0:
                percentage_change_in_price = current_price/average_entry_price
                dollar_change_in_stock = percentage_change_in_price*total_order_cost-total_order_cost
                print('Symbol:', symbol, 'Protecting From A Quick Stop: Average Entry Price', average_entry_price, 'Current Price:', current_price, 'Stop Price', str(round(stop_price, 3)),'Percentage Change', str(round(float(percentage_change_in_price), 5)), 'Dollar Change', ut.round_to_two(float(dollar_change_in_stock)))
            
            
            if float(current_price) <= float(stop_price):
                print("Current Price Lower than stop, trying to sell. current_price:", current_price, "stop_price", stop_price)
                time.sleep(2.4)
                
                cancel_order_info = api.cancel_order(order_id)
                while True:
                    time.sleep(.1)
                    canceled_order_info = api.get_order(order_id)
                    if canceled_order_info.status == 'pending cancel':
                        'PENDING CANCEL, CONTINUING'
                        continue
                    else:
                        break
                    
                quantity_left_to_sell = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
                
                
                if int(quantity_left_to_sell) == 0:
                    print("Hit Stop and Sold Limit... exiting...")
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
                
                order_info = api.get_order(result.id)
                
                quantity_left_to_sell = int(order_info.qty) - int(order_info.filled_qty)
                
                if quantity_left_to_sell == 0:
                    print("Hit Stop and Sold Market... Exiting...")
                    break
                
                else:
                    print("ERROR, something went wrong, should have sold all. Do a Market Order")
            
            time.sleep(.01)
            current_price = ut.get_current_price_of_stock(symbol)    
        
    except KeyboardInterrupt:
        
        ut.cancel_all_symbol_orders(api, symbol)
        
        next_step = input('Would you like to Sell(s) or Change the Stop Loss(c): ')
        
        if next_step == 's':
        
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
            
            sell.sell_the_stock(api, symbol, fraction_of_position_to_sell, False, selling_into_strength)
            
            if fraction_of_position_to_sell != 1:
                
                stop_limit_price = input('Enter New Stop Limit Price: ')
                
                stop.change_stop_loss(api, symbol, stop_limit_price)
                
        
        else:
            
            stop_limit_price = input('Enter New Stop Limit Price: ')
            
            stop.change_stop_loss(api, symbol, stop_limit_price)
            
            
            
        
    
if __name__ == '__main__':

    extended_hours = False
        
    api = tradeapi.REST(
            API_KEY,
            SECRET_KEY,
            BASE_URL
        )
        
        
    symbol = sys.argv[3].upper()
    
    all_orders = api.list_orders()
        
    for order in all_orders:
        if order.symbol == symbol:
            api.cancel_order(order.id)
    
    current_price = ut.get_current_price_of_stock(symbol)
    
    
    
    print(current_price)
    
            
    print('********************* BUYING SCRIPT ***************************')
    print('Symbol: ', symbol, ', current_price:', current_price)
    print('')
    
    if sys.argv[2].isnumeric():
        fraction_of_money_to_spend = float(sys.argv[2])
    else:
        print("ERROR... Fraction Of Money To Spend Should Be an Integer")
    
    
    additional_market_buy = False
    
    if len(sys.argv) > 4 and sys.argv[4] != '0' and sys.argv[4] != '-1':
        #This will be a limit buy
        original_buy_price = float(sys.argv[4])
        factor_over_price_accepted = 1.00025
        stop_out_factor = .998
        limit_buy = True
        print('Limit Buy Tight')
        
    else:
        #This will be a market buy
        original_buy_price = current_price
        factor_over_price_accepted = 1.001
        stop_out_factor = .998
        limit_buy = False
        if sys.argv[4] == '0':
            print('Limit Buy Based On Current Price Plus a Bit')
        if sys.argv[4] == '-1':
            additional_market_buy = True
            print('Limit Buy Based On Current Price Plus a Bit, THEN a Market Buy')
        
        
    
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
    if sys.argv[1] == 'ryan':
        account_portfolio_value = 2500
    if sys.argv[1] == 'chrissy':
        account_portfolio_value = 2500
    
    
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
        stop_loss={'stop_price': stop_price,
                   'limit_price':  limit_price_for_stop}
        )
    
    
    order_id = result.id
    order_qty = result.qty
    
    if additional_market_buy == True:
        
        print('Going to Wait 2 Seconds Then Market Buy')
        time.sleep(2)
        
        cancel_order_info = api.cancel_order(order_id)
        while True:
            time.sleep(.1)
            canceled_order_info = api.get_order(order_id)
            if canceled_order_info.status == 'pending cancel':
                'PENDING CANCEL, CONTINUING'
                continue
            else:
                break
            
        quantity_left_to_buy = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
        
        if quantity_left_to_buy == 0:
            
            order_id = canceled_order_info.legs[0].id    
        
        else:
        
            result = api.submit_order(
                symbol=symbol,
                qty=quantity_left_to_buy,
                side='buy',
                type='market',
                time_in_force='day',
                extended_hours=extended_hours
            )
                
            time.sleep(.2)
            
            result = api.submit_order(
                symbol=symbol,
                qty=original_quantity_to_buy,
                side='sell',
                type='stop_limit',
                time_in_force='day',
                stop_price=stop_price,
                limit_price=limit_price_for_stop,
                extended_hours=extended_hours
            )
            
            order_id = result.id
    
    else:    
        
        try:
            
            for x in range(0,100000):
                
                time.sleep(1)
                
                current_order_info = api.get_order(order_id)
                quantity_left_to_buy = int(current_order_info.qty) - int(current_order_info.filled_qty)
                current_price = ut.get_current_price_of_stock(symbol)
                
                if x%10 == 0:
                    
                    print("Symbol", symbol, "Quantity Left To Buy", quantity_left_to_buy, "Quantity filled:", current_order_info.filled_qty, "Quantity started:", current_order_info.qty)
                    print("Current Price", current_price, "Quantity Left To Buy:", quantity_left_to_buy, "At Price", max_buy_price)
                
                
                current_order_info = api.get_order(current_order_info.id)
                quantity_left_to_buy = int(current_order_info.qty) - int(current_order_info.filled_qty)
                if quantity_left_to_buy == 0:
                    print("Buying Complete, going to check stop loss.")
                    order_id = current_order_info.legs[0].id
                    break
                    
                order_id = current_order_info.id
    
        except KeyboardInterrupt:
            
            print('Canceling All Orders...')
            ut.cancel_all_symbol_orders(api, symbol)
            exit()
            
            
            
    
    current_symbol_position = ut.get_symbol_position(api, symbol)
    average_entry_price = float(current_symbol_position.avg_entry_price)
    current_position_qty = int(current_symbol_position.qty)
    total_order_cost = average_entry_price*current_position_qty
    
        
    
    if entered_stop_price == False:
        stop_price = average_entry_price*stop_out_factor
        
    current_price = ut.get_current_price_of_stock(symbol)
    
    if current_price <= stop_price:
        stop_price = ut.round_to_two(current_price*.9997)
        if float(stop_price) == float(math.floor(current_price * 100)/100.0):
            stop_price = float(stop_price) - .01
        
    
    protect_from_quick_stop(api, symbol, current_price, stop_price, order_id, average_entry_price, total_order_cost)
    