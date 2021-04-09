from _simple_func import load_order_data

with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()
    
def order_list(more_than_one_shop = False):
    '''list products for ordering. '''
    send_text = []
    total = 0
    order_data = load_order_data()
    
    if more_than_one_shop:
        food = []
        food_total = 0
        drink = []
        drink_total = 0
        
    for product in order_data['products']:
        text = '{} {}份 {}元'.format(product, str(order_data['products'][product]['num']), str(order_data['products'][product]['cost']))
        cost = order_data['products'][product]['cost']
        
        if more_than_one_shop:
            if len(product) < 6:
                food.append(text)
                food_total += cost
            else:
                drink.append(text)
                drink_total += cost
        else:    
            send_text.append(text)
            total += cost
            
    if more_than_one_shop:
        for text in food:
            send_text.append(text)
        send_text.append(str(food_total) + '元')
        
        send_text.append('= ' * 3)
        
        for text in drink:
            send_text.append(text)
        send_text.append(str(drink_total) + '元')
    else:
        send_text.append('共{}元'.format(str(total)))
        
    return send_text

def check_list():

    send_text = []
    order_data = load_order_data()
    
    for customer in order_data['customers']:
        send_text.append(customer + ' ' + str(order_data['customers'][customer]['code']))
        
        for product in order_data['customers'][customer]['products']:
            send_text.append('{} x {} {}元'.format(product,
                                                  str(order_data['customers'][customer]['products'][product]['num']),
                                                  str(order_data['customers'][customer]['products'][product]['cost'])
                                                  )
                            )

        send_text.append('=' * 6)
    return send_text
'''
def who_order_drink():
    
    with open('list' + sep + 'order_list.txt', 'w', encoding = 'utf-8') as lfo:
        for name in name_product.keys():
            for product in name_product[name].keys():
                if len(product) > 6:
                    nl.write(' '.join([product, str(name_product[name][product][0] * 5) + '元', '\n-----\n']))
                    
def who_order_food():

    with open('list' + sep + 'order_list.txt', 'w', encoding = 'utf-8') as ol:
        for name in name_product.keys():
            for product in name_product[name].keys():
                if len(product) <= 6:
                    nl.write(' '.join([key, str(name_product[name][product][0] * 5) + '元', '\n-----\n']))
'''
def payment_list():
    send_text = []
    order_data = load_order_data()

    send_text.append('尚 未 付 款')
    send_text.append('- - - - -')
    for customer in order_data['customers']:
        if order_data['customers'][customer]['has_paid'] == False:
            send_text.append('{} {}元'.format(customer, str(order_data['customers'][customer]['personal_total'])))
        
    return send_text
#-------------------------------------------------


