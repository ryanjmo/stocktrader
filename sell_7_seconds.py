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


####   USAGE    ####
#
#python3 sell.py SYMBOL, FRACTION OF POSITION TO SELL, PRICE, STOP_PRICE_OR_FACTOR, FACTOR_OVER_PRICE_ACCEPTED
#
#####################
def sell_the_stock(api, symbol, fraction_of_position_to_sell, extended_hours, selling_into_strength):

    try:    
        print('********************* SELLING SCRIPT ***************************')
        print('Symbol: ', symbol)
    
        if selling_into_strength == True:
            sell_factor = 1.002
            walk_down_factor = 7
            
            
        all_orders = api.list_orders()
        
        for order in all_orders:
            if order.symbol == symbol:
                api.cancel_order(order.id)
        
        original_symbol_position = ut.get_symbol_position(api, symbol)
        
        print("Original Symbol Position:", original_symbol_position)
        if original_symbol_position == 0:
            print("No Symbol Position.. Exiting...")
            exit()
        original_position_qty = int(original_symbol_position.qty)
        
        original_symbol_price = ut.get_current_price_of_stock(symbol)    
        
        print('original_position_qty', original_position_qty)
        print('original_symbol_price', original_symbol_price)
        
        
        if selling_into_strength == True:
            max_sell_price = ut.round_to_two((original_symbol_price)*sell_factor)
            print('sell_factor', sell_factor)
            print('max_sell_price', max_sell_price)
        
        print('Selling Program Started...')
        
        original_quantity_to_sell = int(original_position_qty/fraction_of_position_to_sell)
        
        print('Quantity of ', symbol ,' Trying To Sell: ', int(original_quantity_to_sell))
        print('')
        
        if selling_into_strength == False:
            
            print('Not Selling into strength, putting in Limit Order for 4 seconds. Limit price:', original_symbol_price)
            result = api.submit_order(
                symbol=symbol,
                qty=original_quantity_to_sell,
                side='sell',
                type='limit',
                time_in_force='day',
                limit_price=original_symbol_price,
                extended_hours=extended_hours
            )
            
            time.sleep(3.9)
            
            order_id = result.id
            
            while True:
                cancel_order_info = api.cancel_order(order_id)
                time.sleep(.1)
                canceled_order_info = api.get_order(order_id)
                if canceled_order_info.status == 'pending cancel':
                    'PENDING CANCEL, CONTINUING'
                    continue
                else:
                    break
                
            quantity_left_to_sell = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
            
            if int(quantity_left_to_sell) == 0:
                
                print("Sold All With Limit, Exiting...")
                
            else:
                print("Didn't sell all doing market sell")
                result = api.submit_order(
                    symbol=symbol,
                    qty=original_quantity_to_sell,
                    side='sell',
                    type='market',
                    time_in_force='day',
                    extended_hours=extended_hours
                )
                time.sleep(2)
                market_order_info = api.get_order(order_id)
                quantity_left_to_sell = int(market_order_info.qty) - int(market_order_info.filled_qty)
                if quantity_left_to_sell == 0:
                    print("All sold from market... exiting...")
                else:
                    print("Error, should have all sold market... look into this")
                
        else:
            order_infos = {}
            price_divisions = 3
            single_price_factor = 1/price_divisions
            total_quantity_put_into_orders = 0
            sell_factor_decimal = (sell_factor-1)
            
            for x in range(0,price_divisions):
                order_infos[x] = {}
                fraction_of_price_factor = x/(price_divisions-1)
                new_sell_factor = (sell_factor-1)*fraction_of_price_factor
                raw_price_for_order = float((1+new_sell_factor)*original_symbol_price)
                price_for_order = ut.round_to_two((1+new_sell_factor)*original_symbol_price)
                print('iteration', x, 'price_for_order', price_for_order)
                if x == price_divisions - 1:
                    quantity_to_sell_this_itteration = original_quantity_to_sell-total_quantity_put_into_orders
                else:
                    quantity_to_sell_this_itteration = original_quantity_to_sell/price_divisions
                
                quantity_to_sell_this_itteration = int(quantity_to_sell_this_itteration)
                total_quantity_put_into_orders += quantity_to_sell_this_itteration
                if quantity_to_sell_this_itteration == 0:
                    order_infos[x]['qty'] = 0
                    continue
                result = api.submit_order(
                    symbol=symbol,
                        qty=quantity_to_sell_this_itteration,
                        side='sell',
                        type='limit',
                        time_in_force='day',
                        limit_price=price_for_order,
                        extended_hours=extended_hours
                        
                    )
                    
                order_infos[x]['id'] = result.id
                order_infos[x]['qty'] = int(result.qty)
                order_infos[x]['price'] = float(result.limit_price)
                order_infos[x]['raw_price_for_order'] = raw_price_for_order
                print('Selling...', symbol, 'Quantity', order_infos[x]['qty'], 'Price', order_infos[x]['price'])
                
                if int(int(result.qty) != int(quantity_to_sell_this_itteration)):
                    print("ERROR, result.qty and quantity_to_sell_this_itteration should be the same")
                    
                    
            
            start = time.time()
            
            for x in range(0,100000):
                itteration = x%price_divisions
                print("Selling:", symbol, "Itteration:", itteration)
                if x%price_divisions == 0:
                    end = time.time()
                    print('Time Elapsed:', end - start)
                time.sleep(.25)
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
                
                cancel_order_info = api.cancel_order(order_info['id'])
                time.sleep(.25)
                canceled_order_info = api.get_order(order_info['id'])
                if canceled_order_info.status == 'pending cancel':
                    'PENDING CANCEL, CONTINUING'
                    continue
                quantity_left_to_sell = int(canceled_order_info.qty) - int(canceled_order_info.filled_qty)
                previous_price = order_info['price']
                previous_raw_price_for_order = order_info['raw_price_for_order']
                raw_price_for_order = float(previous_raw_price_for_order-(sell_factor-1)*previous_raw_price_for_order/walk_down_factor)
                order_info['raw_price_for_order'] = raw_price_for_order
                price_for_order = ut.round_to_two(previous_raw_price_for_order-(sell_factor-1)*previous_raw_price_for_order/walk_down_factor)
                order_info['price'] = float(price_for_order)
                current_price = ut.get_current_price_of_stock(symbol)
                print("Symbol", symbol, "Quantity filled:", canceled_order_info.filled_qty, "Quantity started:", canceled_order_info.qty, "Left To Sell:", quantity_left_to_sell)
                print('reduce price by', ut.round_to_two((sell_factor-1)*order_info['price']/walk_down_factor), 'Previous Price:', previous_price, "New Price:", order_info['price'], 'Raw Price For Order', order_info['raw_price_for_order'])
                print("Current Price:", current_price)
                
                if quantity_left_to_sell == 0:
                    order_info['qty'] = 0
                    print('Quantity Zero, Skipping Itteration:', itteration)
                    continue
                
               
                try:
                    result = api.submit_order(
                        symbol=symbol,
                        qty=quantity_left_to_sell,
                        side='sell',
                        type='limit',
                        limit_price=order_info['price'],
                        time_in_force='day',
                        extended_hours=extended_hours
                    )
                except Exception as e:  
                    ut.print_error(e)
                    print('ERROR Selling...')
                    continue
                    
                    
                order_info['id'] = result.id
                order_info['qty'] = result.qty
            
        
    except KeyboardInterrupt:
        
        all_orders = api.list_orders()
    
        for order in all_orders:
            if order.symbol == symbol:
                api.cancel_order(order.id)
                
        original_symbol_position = ut.get_symbol_position(api, symbol)
        
        if original_symbol_position == 0:
            print("All Sold out Exiting....")
        else:
            print("Doing a Market Sell...")
            result = api.submit_order(
                symbol=symbol,
                qty=original_symbol_position,
                side='sell',
                type='market',
                time_in_force='day',
                extended_hours=extended_hours
            )
                
     
    exit()  
        

if __name__ == '__main__':
    
    extended_hours = False
    
    symbol = sys.argv[2].upper()
    
    print('********************* SELLING SCRIPT ***************************')
    print('Symbol: ', symbol)
    print('')
    
    current_price = ut.get_current_price_of_stock(symbol)
    
    api = tradeapi.REST(
            API_KEY,
            SECRET_KEY,
            BASE_URL
        )
        
        
    if len(sys.argv) > 3:
        if sys.argv[3] == 'n':
            selling_into_strength = False
        else:
            selling_into_strength = True
    else:
        selling_into_strength = True

    if len(sys.argv) > 4:
        if sys.argv[4].isnumeric():
            fraction_of_position_to_sell = int(sys.argv[3])
        else:
            print("ERROR... Fraction Of Position To Sell Should Be an Integer")
    else:
        fraction_of_position_to_sell = 1
        
    
        
    
    sell_the_stock(api, symbol, fraction_of_position_to_sell, extended_hours, selling_into_strength)