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
    buy_factor = .999
    walk_down_factor = 3
    
else:
    #This will be a market buy
    original_buy_price = current_price
    factor_over_price_accepted = 1.001
    stop_out_factor = .998
    buy_factor = .9985
    walk_down_factor = 2
    
    
    

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


current_quantity_to_buy = original_quantity_to_buy

print('max_buy_price', max_buy_price, 'limit_price_for_stop', limit_price_for_stop, 'Estimated stop_price', stop_price)

order_infos = {}
price_divisions = 7
single_price_factor = 1/price_divisions
total_quantity_put_into_orders = 0
buy_factor_decimal = (buy_factor-1)


for x in range(0,price_divisions):
    order_infos[x] = {}
    fraction_of_price_factor = x/(price_divisions-1)
    new_buy_factor = (buy_factor-1)*fraction_of_price_factor
    raw_price_for_order = float((1+new_buy_factor)*original_buy_price)
    price_for_order = ut.round_to_two(raw_price_for_order)
    
    print('iteration', x, 'price_for_order', price_for_order)
    if x == price_divisions - 1:
        quantity_to_buy_this_itteration = original_quantity_to_buy-total_quantity_put_into_orders
    else:
        quantity_to_buy_this_itteration = original_quantity_to_buy/price_divisions
    
    quantity_to_buy_this_itteration = int(quantity_to_buy_this_itteration)
    total_quantity_put_into_orders += quantity_to_buy_this_itteration
    result = api.submit_order(
        symbol=symbol,
            qty=quantity_to_buy_this_itteration,
            side='buy',
            type='limit',
            time_in_force='day',
            limit_price=price_for_order,
            extended_hours=extended_hours
        )
        
    order_infos[x]['id'] = result.id
    order_infos[x]['qty'] = int(result.qty)
    order_infos[x]['price'] = float(result.limit_price)
    order_infos[x]['raw_price_for_order'] = raw_price_for_order
    print('Buying...', symbol, 'Quantity', order_infos[x]['qty'], 'Price', order_infos[x]['price'], "Raw Price", order_infos[x]['raw_price_for_order'])
    
    if int(int(result.qty) != int(quantity_to_buy_this_itteration)):
        print("ERROR, result.qty and quantity_to_buy_this_itteration should be the same")
        

start = time.time()

for x in range(0,100000):
    
    if x%price_divisions == 0:
        end = time.time()
        print('')
        print('Time Elapsed:', end - start)
    time.sleep(.25)
    itteration = x%price_divisions
    print("Buying:", symbol, "Itteration:", itteration)
    order_info = order_infos[itteration]
    
    if order_info['qty'] == 0:
        print('Quantity Zero, Skipping Itteration:', itteration)
        
        all_zeros = True
        for x in range(0, price_divisions):
            if order_infos[x]['qty'] != 0:
                all_zeros = False
        
        if all_zeros == True:
            break
        else:
            continue
    
    if ut.round_to_two(order_info['price']) >= ut.round_to_two(float(max_buy_price)):
        current_order_info = api.get_order(order_info['id'])
        quantity_left_to_buy = int(current_order_info.qty) - int(current_order_info.filled_qty)
        order_info['qty'] = quantity_left_to_buy
        if quantity_left_to_buy == 0:
            print('Quantity Zero, Skipping:', itteration)
            continue
        print('Already At Max Price,',  max_buy_price, ' Skipping:', itteration)
        current_price = ut.get_current_price_of_stock(symbol)
        print('Current Price:', current_price)
        time.sleep(.25)
        continue
    cancel_order_info = api.cancel_order(order_info['id'])
    time.sleep(.25)
    canceled_order_info = api.get_order(order_info['id'])
    if canceled_order_info.status == 'pending cancel':
        'PENDING CANCEL, CONTINUING'
        continue
    quantity_left_to_buy = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
    
    
    if quantity_left_to_buy == 0:
        order_info['qty'] = 0
        print('Quantity Zero, Skipping:', itteration)
        continue
        
    
    old_raw_price_for_order = order_info['raw_price_for_order']
    previous_price = order_info['price']
    raw_price_for_order = float(old_raw_price_for_order-(buy_factor-1)*old_raw_price_for_order/walk_down_factor)
    order_info['raw_price_for_order'] = raw_price_for_order
    price_for_order = ut.round_to_two(old_raw_price_for_order-(buy_factor-1)*old_raw_price_for_order/walk_down_factor)
    order_info['price'] = float(price_for_order)
    price_for_order = min(price_for_order, max_buy_price)
    current_price = ut.get_current_price_of_stock(symbol)
    print("Symbol", symbol, "Quantity filled:", canceled_order_info.filled_qty, "Quantity started:", canceled_order_info.qty)
    print('reduce price by', ut.round_to_two((buy_factor-1)*order_info['price']/walk_down_factor), 'Previous Price:', previous_price, "Raw New Price", order_info['raw_price_for_order'],   "New Price:", order_info['price'])
    print("Current Price", current_price, "Quantity Left To Buy:", quantity_left_to_buy, "At Price", order_info['price'], 'iteration x%price_divisions', x%price_divisions)
    
    
    
    try:
        result = api.submit_order(
            symbol=symbol,
            qty=quantity_left_to_buy,
            side='buy',
            type='limit',
            time_in_force='day',
            limit_price=order_info['price'],
            extended_hours=extended_hours
        )
    except Exception as e:  
        ut.print_error(e)
        print('ERROR Buying...')
        buying_error = True
        continue
    
    order_info['id'] = result.id
    order_info['qty'] = result.qty
    print('Buying Symbol', symbol, "Quantity", order_info['qty'], 'at price', order_info['price'] )
    
  

current_symbol_position = ut.get_symbol_position(api, symbol)
average_entry_price = float(current_symbol_position.avg_entry_price)
current_position_qty = int(current_symbol_position.qty)

if current_position_qty == 0:
    print("Error: There is no qty for this symbol and their should be because we just bought a bunch")
    exit()

if entered_stop_price == False:
    stop_price = average_entry_price*stop_out_factor
    
current_price = ut.get_current_price_of_stock(symbol)

if current_price <= stop_price:
    stop_price = ut.round_to_two(current_price*.9997)
    if float(stop_price) == float(math.floor(current_price * 100)/100.0):
        stop_price = float(stop_price) - .01
    

try:
    for x in range(0,100000):
    
        ##check to see if price is under and if so sell
        
        if x == 0:
            print('Symbol:', symbol, 'Protecting From A Quick Stop: Average Entry Price', average_entry_price, 'Current Price:', current_price, 'Stop Price', stop_price)
        
        
        if float(current_price) <= float(stop_price):
            print('Stop Hit... Selling... Symbol:', symbol, 'Protecting From A Quick Stop: Average Entry Price', average_entry_price, 'Current Price:', current_price, 'Stop Price', stop_price)
            sell.sell_the_stock(api, symbol, 1, extended_hours, False)
           
            
        if (x%100 == 0):
            print('Symbol:', symbol, 'Protecting From A Quick Stop: Average Entry Price', average_entry_price, 'Current Price:', current_price, 'Stop Price', stop_price)
        time.sleep(.01) 
        
        current_price = ut.get_current_price_of_stock(symbol)
except KeyboardInterrupt:
    
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

    