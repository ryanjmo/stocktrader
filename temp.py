while True:
    try:
        result = api.submit_order(
            symbol=symbol,
            qty=quantity_left_to_sell,
            side='sell',
            type='limit',
            time_in_force='gtc',
            limit_price=order_info['price']
        )
        break
    except Exception as e:  
        print('ERROR SELLING...')
        quantity_left_to_sell = ut.calculate_quanity_left_to_sell(api, order_info)
        
        if quantity_left_to_sell == 0:
            order_info['qty'] = 0
            break
        time.sleep(2)