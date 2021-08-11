import sys
if sys.argv[1] == 'ryan':
    from config import *
    import config as config
if sys.argv[1] == 'chrissy':
    from config_chrissy import *
    import config_chrissy as config
import os
import asyncio
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
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
import logging
import threading

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


##change
####   USAGE    ####
#
#python3 buy.py NAME, SYMBOL, FACTOR_OF_MONEY_TO_SPEND, PRICE, STOP_PRICE
#
#####################

def set_buy_script_variables_and_buy(api, symbol, prices_for_entry):
    
    limit_buy = True    
                    
    if prices_for_entry['long_or_short'] == 'l':
        is_long = True
    elif prices_for_entry['long_or_short'] == 's':
        is_long = False
    
    stop_price = prices_for_entry['stop_price']
        
    original_buy_price = prices_for_entry['price_to_enter']
    current_price = prices_for_entry['current_price']
    stop_out_factor = prices_for_entry['stop_out_factor']


    entered_stop_price = False
    
    buy_script(api, symbol, is_long, 1, False, original_buy_price, stop_price, current_price, True, 0, True)
    

def set_enter_price_and_stop(current_price, long_or_short):
    
    if long_or_short == 'l':
        factor_over_price_accepted = 1.00025
        stop_out_factor = .985
    elif long_or_short == 's':
        factor_over_price_accepted = .99975
        stop_out_factor = 1.015 
    
    
    price_to_enter = ut.move_price_at_least_three_cents(current_price, factor_over_price_accepted)
        
    stop_price = ut.move_price_at_least_one_cent(current_price, stop_out_factor)  
        
    prices_for_entry = {}
    
    prices_for_entry['price_to_enter'] = price_to_enter
    prices_for_entry['stop_price'] = stop_price
    prices_for_entry['current_price'] = current_price
    prices_for_entry['long_or_short'] = long_or_short
    prices_for_entry['factor_over_price_accepted'] = factor_over_price_accepted
    prices_for_entry['stop_out_factor'] = stop_out_factor
    
    return prices_for_entry
    
def get_new_stop_and_reverse(stop_price, average_entry_price):
    
    new_entered_stop_price = input('Current Stop Loss is ' + str(stop_price) + ' Average Entry Price Was ' + str(ut.round_to_two(average_entry_price)) + ' Press ENTER to continue, enter new price for new stop loss: ')
        
    try:
        
        float(new_entered_stop_price)
        stop_price = float(new_entered_stop_price)
        print("New Stop Entered... New Stop is: ", stop_price)
        entered_stop_price = True
        
    except ValueError:
        print('No New Stop Entered.. Stop is: ', stop_price)
    
    
    while True:
        reverse_on_stop = input("Do you want to reverse the trade if it hits the stop loss YES(y) or NO(n):")
        if reverse_on_stop == 'y' or reverse_on_stop == 'n':
            break
    
    new_stop_and_reverse = {}
    new_stop_and_reverse['stop_price'] = stop_price
    new_stop_and_reverse['reverse_on_stop'] = reverse_on_stop
    return new_stop_and_reverse
 
def get_price_to_enter(api, symbol):
    
    print('Determining Price On The Fly... press ctrl-c to trade')
    
    try:
        while True:
            current_price = ut.get_current_price_of_stock(symbol)    
            print(current_price)
            time.sleep(.1)
        
    
    except KeyboardInterrupt:
        
        
        while True:
        
            long_or_short = input('Price is ' + str(current_price) + ' Press l for long, s for short. Press ctrl+c to exit program without trading.')
            if long_or_short == 'l' or long_or_short == 's':
                break
        
        prices_for_entry = set_enter_price_and_stop(current_price, long_or_short)
        
        return prices_for_entry
                    
    
def protect_from_quick_stop(api, symbol, current_price, stop_price, order_id, average_entry_price, total_order_cost, entry_side, exit_side, need_to_update_stop, reverse_on_stop):
    
    if entry_side == 'buy':
        is_long = True
    else:
        is_long = False
    
    stop_price = float(stop_price)
    
    extended_hours = False
    
    try:
        for x in range(0,100000):
            
            if need_to_update_stop == True:
                need_to_update_stop = False
                order_id = stop.change_stop_loss(api, symbol, stop_price)
                current_price = ut.get_current_price_of_stock(symbol)
                
        
            ##check to see if price is under and if so sell
            
            if x%50 == 0:
                original_symbol_position = ut.get_symbol_position(api, symbol)
                if original_symbol_position == 0:
                    print("No Symbol Position.. Exiting...")
                    exit()
                original_position_qty = int(original_symbol_position.qty)
                percentage_change_in_price = current_price/average_entry_price
                dollar_change_in_stock = percentage_change_in_price*total_order_cost-total_order_cost
                print('Symbol:', symbol, 'Protecting From A Quick Stop: Average Entry Price', average_entry_price, 'Current Price:', current_price, 'Stop Price', str(round(stop_price, 3)),'Percentage Change', str(round(float(percentage_change_in_price), 5)), 'Dollar Change', ut.round_to_two(float(dollar_change_in_stock)), 'original_position_qty', original_position_qty)
            
            
            if (is_long == True and float(current_price) <= float(stop_price)) or (is_long == False and float(current_price) >= float(stop_price)):
                print("Current Price Beyond Stop Price, trying to Exit. current_price:", current_price, "stop_price", stop_price)
                
                start = time.time()
                if reverse_on_stop == 'y':
                    break_after_time = .5
                else:
                    break_after_time = 4.1
                
                while True:
                
                    order_info = api.get_order(order_id)
                    
                    quantity_left_to_sell = int(order_info.qty) - int(order_info.filled_qty)
                
                    if int(quantity_left_to_sell) == 0:
                        break
                    
                    end = time.time()
                    
                    print('end - start: ', end - start)
                    
                    if float(end - start) > break_after_time:
                        break
                    
                    time.sleep(.15)
                
                cancel_exorder_info = api.cancel_order(order_id)
                
                while True:
                    time.sleep(.1)
                    canceled_order_info = api.get_order(order_id)
                    if canceled_order_info.status == 'pending cancel':
                        'PENDING CANCEL, CONTINUING'
                        continue
                    else:
                        break
                
                time.sleep(.2)    
                    
                quantity_left_to_sell = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
                
                
                if int(quantity_left_to_sell) == 0:
                    print("Hit Stop and Sold Limit... exiting...")
                    break
                
                try:
                
                    result = api.submit_order(
                            symbol=symbol,
                            qty=quantity_left_to_sell,
                            side=exit_side,
                            type='market',
                            time_in_force='day',
                            extended_hours=extended_hours,
                        )
                except Exception as e: 
                    
                    ut.cancel_all_symbol_orders(api, symbol)
                    current_symbol_position = ut.get_symbol_position(api, symbol)
            
                    if current_symbol_position == 0:
                        print("Hit Stop and Sold Market... Exiting...")
                        break
                    
                    quantity_left_to_sell = int(current_symbol_position.qty)
                    
                    result = api.submit_order(
                        symbol=symbol,
                        qty=abs(quantity_left_to_sell),
                        side=exit_side,
                        type='market',
                        time_in_force='day',
                        extended_hours=extended_hours,
                    )
                
                time.sleep(1)
                
                order_info = api.get_order(result.id)
                
                quantity_left_to_sell = int(order_info.qty) - int(order_info.filled_qty)
                
                if quantity_left_to_sell == 0:
                    print("Hit Stop and Sold Market... Returning To Trade")
                    break
                
                else:
                    print("ERROR, something went wrong, should have sold all. Do a Market Order")
            
            time.sleep(.2)
            current_price = ut.get_current_price_of_stock(symbol)
            
            print(symbol, 'current price :', current_price, 'Average Entry Price', average_entry_price, 'Stop Price', str(round(stop_price, 3)))
            
        
    except KeyboardInterrupt:
        
        ut.cancel_all_symbol_orders(api, symbol)
        
        try:
            while True:
                next_step = input('Would you like to Sell(s) or Reverse Trade Direction (r) or Buy More (b) or Change the Stop Loss(c): ')
                if next_step == 's' or next_step == 'r' or next_step == 'b' or next_step == 'c':
                    break
        except KeyboardInterrupt:
            exit()
        
        if next_step == 's' or next_step == 'r':
        
            if next_step == 's':
                while True:
                    fraction_of_position_to_sell = input('Enter Fraction Of Position You Want Sold: ')
                    
                    if fraction_of_position_to_sell.isnumeric():
                        fraction_of_position_to_sell = float(fraction_of_position_to_sell)
                        break
                
            elif next_step == 'r':
                
                fraction_of_position_to_sell = 1
            
                
            
            while True:
                selling_into_strength_input = input('Selling Into Strength. Yes(y) or No(n) or Sell Now (s) or Set Limit (l): ')
                if selling_into_strength_input == 'y' or selling_into_strength_input == 'n' or selling_into_strength_input == 'l' or selling_into_strength_input == 's':
                    break
           
            limit_price_for_sale = 0
            if selling_into_strength_input == 'l':
               limit_price_for_sale = input('Enter Limit Price For Sale: ')
            
            sell.sell_the_stock(api, symbol, fraction_of_position_to_sell, False, selling_into_strength_input, limit_price_for_sale, original_position_qty)
            
            current_symbol_position = ut.get_symbol_position(api, symbol)
            
            if current_symbol_position == 0:
                
                print("Entire Position Sold, Going to trade")
                
                if next_step == 'r':
                    
                    current_price = ut.get_current_price_of_stock(symbol)    
                    
                    print("Entering at This current price, current_price", current_price)
                    
                    #switch entry side to other because we are reversing direction
                    if entry_side == 'buy':
                        long_or_short = 's'
                    else:
                        long_or_short = 'l'
                    
                    prices_for_entry = set_enter_price_and_stop(current_price, long_or_short)
                    
                    
                else:
            
                    print('Determining Price On The Fly For Trade...')
                    
                    prices_for_entry = get_price_to_enter(api, symbol)
                    
                
                set_buy_script_variables_and_buy(api, symbol, prices_for_entry)
                
                
                 
            else:    
                
                new_stop_and_reverse = get_new_stop_and_reverse(stop_price, average_entry_price)
                need_to_update_stop = True
                protect_from_quick_stop(api, symbol, current_price, new_stop_and_reverse['stop_price'], order_id, average_entry_price, total_order_cost, entry_side, exit_side, need_to_update_stop, new_stop_and_reverse['reverse_on_stop'])
                
        
        elif next_step == 'c':
            #next_step was c change stop loss
            new_stop_and_reverse = get_new_stop_and_reverse(stop_price, average_entry_price)
            need_to_update_stop = True
            protect_from_quick_stop(api, symbol, current_price, new_stop_and_reverse['stop_price'], order_id, average_entry_price, total_order_cost, entry_side, exit_side, need_to_update_stop, new_stop_and_reverse['reverse_on_stop'])
        
        elif next_step == 'b':
            if is_long == True:
                long_or_short = 'l'
            else:
                long_or_short = 's'
            current_price = ut.get_current_price_of_stock(symbol)
            prices_for_entry = set_enter_price_and_stop(current_price, long_or_short)
            set_buy_script_variables_and_buy(api, symbol, prices_for_entry)
    
    if reverse_on_stop == 'y':
        #reverse direction
        if is_long == True:
            long_or_short = 's'
        else:
            long_or_short = 'l'
            
        current_price = ut.get_current_price_of_stock(symbol)
        prices_for_entry = set_enter_price_and_stop(current_price, long_or_short)
        set_buy_script_variables_and_buy(api, symbol, prices_for_entry)
        
    else:
        prices_for_entry = get_price_to_enter(api, symbol)
        set_buy_script_variables_and_buy(api, symbol, prices_for_entry)
    
            
            

def buy_script(api, symbol, is_long, fraction_of_money_to_spend, additional_market_buy, original_buy_price, stop_price, current_price, entered_stop_price, stop_out_factor, on_the_fly):

    extended_hours = False

    print('********************* BUYING SCRIPT ***************************')
    print('Symbol: ', symbol, ', current_price:', current_price)
    print('')
        
    if is_long == True:
        factor_over_price_accepted = 1.00025
        limit_factor = .9995
    else:
        factor_over_price_accepted = .99975
        limit_factor = 1.0005
        
    #limit_price_for_stop = stop_price*.998
    #limit_price_for_stop = stop_price*1
    limit_price_for_stop = ut.move_price_at_least_one_cent(stop_price, limit_factor)

    
    max_buy_price = ut.round_to_two((original_buy_price)*factor_over_price_accepted)
    
    print('Buying Program Started...')
    print('Target Buy Price:', original_buy_price)
    print('Maximum Buy Price', max_buy_price)
    print('Stop Factor:', stop_out_factor)
    print('Estimated Stop Out Price', ut.round_to_two(stop_price))
    print('Limit Price', ut.round_to_two(limit_price_for_stop))
    
    
    
    if sys.argv[1] == 'ryan':
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
    if sys.argv[1] == 'chrissy':
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
    
    
    original_quantity_to_buy = (float(config.position_size)/fraction_of_money_to_spend)/float(max_buy_price)
    
    original_quantity_to_buy = int(original_quantity_to_buy)
    print('Quantity of ', symbol ,' Trying To Buy: ', int(original_quantity_to_buy))
    print('Maximum Cost of Order: ', ut.round_to_two((original_quantity_to_buy) * float(max_buy_price)))
    print('')
    
    if is_long == True:
        entry_side = 'buy'
        exit_side = 'sell'
        
    else:
        entry_side = 'sell'
        exit_side = 'buy'
    
    result = api.submit_order(
        symbol=symbol,
        qty=original_quantity_to_buy,
        side=entry_side,
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
        
        canceled_order_info = ut.get_cancled_order_info(api, order_id)
            
        quantity_left_to_buy = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
        
        if quantity_left_to_buy == 0:
            
            order_id = canceled_order_info.legs[0].id    
        
        else:
        
            result = api.submit_order(
                symbol=symbol,
                qty=quantity_left_to_buy,
                side=entry_side,
                type='market',
                time_in_force='day',
                extended_hours=extended_hours
            )
                
            time.sleep(.2)
            
            while True:
                try:
                    result = api.submit_order(
                        symbol=symbol,
                        qty=original_quantity_to_buy,
                        side=exit_side,
                        type='stop_limit',
                        time_in_force='day',
                        stop_price=stop_price,
                        limit_price=limit_price_for_stop,
                        extended_hours=extended_hours
                    )
                    break
                except Exception as e:
                    print(e)
                    print("error putting stop... trying to put stop again...")
                    time.sleep(.1)
            
            
                
            
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
    
    print("******current position info", original_quantity_to_buy, current_position_qty)
    if float(abs(original_quantity_to_buy)) != float(abs(current_position_qty)) and float(abs(current_position_qty)) > float(abs(original_quantity_to_buy)):
        print("PLEASE NOTE: original_quantity_to_buy is not equal to current_position_qty. Canceling Stop Order and putting in new one.")
        canceled_order_info = ut.get_cancled_order_info(api, order_id)
        
        current_symbol_position = ut.get_symbol_position(api, symbol)
        average_entry_price = float(current_symbol_position.avg_entry_price)
        current_position_qty = int(current_symbol_position.qty)
        
        while True:
            try:
                result = api.submit_order(
                    symbol=symbol,
                    qty=abs(current_position_qty),
                    side=exit_side,
                    type='stop_limit',
                    time_in_force='day',
                    stop_price=stop_price,
                    limit_price=limit_price_for_stop,
                    extended_hours=extended_hours
                )
                break
            except Exception as e:
                print(e)
                print("error putting stop... trying to put stop again...")
                time.sleep(.1)
        
    reverse_on_stop = 'n'
    
    if on_the_fly == True:
        
        new_stop_and_reverse = get_new_stop_and_reverse(stop_price, average_entry_price)
        stop_price = new_stop_and_reverse['stop_price']
        reverse_on_stop = new_stop_and_reverse['reverse_on_stop']
        
    
    total_order_cost = average_entry_price*current_position_qty
    
        
    
    if entered_stop_price == False:
        stop_price = ut.move_price_at_least_one_cent(stop_out_factor, average_entry_price)
        
    current_price = ut.get_current_price_of_stock(symbol)
    
    need_to_update_stop = True
    protect_from_quick_stop(api, symbol, current_price, stop_price, order_id, average_entry_price, total_order_cost, entry_side, exit_side, need_to_update_stop, reverse_on_stop)


async def print_trade(trade):
    if trade.tape == 'C':
        config.current_price = float(trade.price)
        #print(config.current_price)
        
def price_getting_thread(symbol):
    
    try:
        # make sure we have an event loop, if not create a new one
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
        
    logging.basicConfig(level=logging.INFO)
    stream = Stream(API_KEY,
                  SECRET_KEY,
                  base_url=URL(BASE_URL),
                  data_feed='sip')
    stream.subscribe_trades(print_trade, symbol)
    
    stream.run()
        
    
if __name__ == '__main__':

    extended_hours = False
        
    api = tradeapi.REST(
            API_KEY,
            SECRET_KEY,
            BASE_URL
        )
        
    symbol = sys.argv[4].upper()
    
    position_size = input('How much do you want to bet. BE SAMART:')
    
    config.init_globals(position_size)
    
    threading.Thread(target=price_getting_thread, kwargs={'symbol': symbol}).start()
    
    
    print('current_price', config.current_price)
    
    all_orders = api.list_orders()
        
    for order in all_orders:
        if order.symbol == symbol:
            api.cancel_order(order.id)

    if sys.argv[1] == 'ryan':
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
        print("RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN RYAN")
    if sys.argv[1] == 'chrissy':
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")
        print("CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY CHRISSY")

    
    is_long = True
    
    if sys.argv[2] == 'long':
        is_long = True
    elif sys.argv[2] == 'short':
        is_long = False
    else:
        print("Need to Enter Long Or Short")
    
    
    if sys.argv[3].isnumeric():
        fraction_of_money_to_spend = float(sys.argv[3])
    else:
        print("ERROR... Fraction Of Money To Spend Should Be an Integer")
    
    
    additional_market_buy = False
    on_the_fly = False
    
    if len(sys.argv) > 5 and sys.argv[5] != '0' and sys.argv[5] != '-1' and sys.argv[5] != '-2':
        #This will be a limit buy
        original_buy_price = float(sys.argv[5])
        
        if is_long == True:
            if float(original_buy_price) < 20:
                factor_over_price_accepted = 1.001
                stop_out_factor = .985
            elif float(original_buy_price) < 100:
                factor_over_price_accepted = 1.0005
                stop_out_factor = .9925
            else:
                factor_over_price_accepted = 1.00025
                stop_out_factor = .998
            
        else:
            if float(original_buy_price) < 20:
                factor_over_price_accepted = .999
                stop_out_factor = 1.015
            elif float(original_buy_price) < 100:
                factor_over_price_accepted = .9995
                stop_out_factor = 1.0075
            else:
                factor_over_price_accepted = .99975
                stop_out_factor = 1.002
                
        limit_buy = True
        print('Limit Buy Tight')
        current_price = -1
        
    elif sys.argv[5] == '0' or sys.argv[5] == '-1':
        
        #This will be a market buy
        current_price = ut.get_current_price_of_stock(symbol)
        original_buy_price = current_price
        if is_long == True:
            factor_over_price_accepted = 1.001
            stop_out_factor = .998
        else:
            factor_over_price_accepted = .999
            stop_out_factor = 1.002

            
        limit_buy = False
        if sys.argv[5] == '0':
            print('Limit Buy Based On Current Price Plus a Bit')
        if sys.argv[5] == '-1':
            additional_market_buy = True
            print('Limit Buy Based On Current Price Plus a Bit, THEN a Market Buy')
            
    else:
        
        #determine price on the fly
        on_the_fly = True
        
        limit_buy = True
        
        
        prices_for_entry = get_price_to_enter(api, symbol)
        
        if len(sys.argv) <= 6:
            stop_price = prices_for_entry['stop_price']
            sys.argv.append(stop_price)
            entered_stop_price = True
            
        if prices_for_entry['long_or_short'] == 'l':
            is_long = True
        elif prices_for_entry['long_or_short'] == 's':
            is_long = False
            
        original_buy_price = prices_for_entry['price_to_enter']
        current_price = prices_for_entry['current_price']
        stop_out_factor = prices_for_entry['stop_out_factor']
    
    
    if len(sys.argv) > 6:
        entered_stop_price = True
        stop_price  = float(sys.argv[6])
        
    elif on_the_fly == False:
        entered_stop_price = False
        stop_price = float(original_buy_price)*stop_out_factor
        
    
    buy_script(api, symbol, is_long, fraction_of_money_to_spend, additional_market_buy, original_buy_price, stop_price, current_price, entered_stop_price, stop_out_factor, on_the_fly)
    
    