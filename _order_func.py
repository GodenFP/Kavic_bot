import json

with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()


def load_order_data():
    #try:
        with open('Data' + sep + 'order_data.json', encoding = 'utf-8') as js:
            return json.load(js)      
    #except:
        print('Can\'t load order_data.')

def dump_order_data(data):
    try:
        with open('Data' + sep + 'order_data.json', 'w', encoding = 'utf-8') as js:
            json.dump(data, js, ensure_ascii = False, indent = 4)
            
    except:
        print('Can\'t dump order_data.')

def count_product():
    order_data = load_order_data()
    products = {}

    for customer in order_data['customers']:
        for product in order_data['customers'][customer]['products']:
            product_data = order_data['customers'][customer]['products'][product]
            if product not in products:
                products[product] = {
                        'num' : product_data['num'],
                        'cost' : product_data['cost']}
            else:
                products[product]['num'] += product_data['num']
                products[product]['cost'] += product_data['cost']
    return products

def order_list():
    '''
    Make a list of products for ordering.
    If more_than_one_shop is True,
    this func will judge the length of product's name.
    Greater than 6, the product will be classified as 'drink',
    otherwise, food(not accurate)
    Return a list of texts to send.
    '''
    send_text = []
    total = 0
    products = count_product()
    more_than_one_shop = (len(load_order_data()['shops']) > 1)
    
    if more_than_one_shop:
        food = []
        food_total = 0
        drink = []
        drink_total = 0
        
    for product in products:
        text = '{} {}份 {}元'.format(product, str(products[product]['num']), str(products[product]['cost']))
        cost = products[product]['cost']
        
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
    '''
    Make a list of who ordered, ordered what,
    and how much the personal total is.
    Return a list of texts to send.
    '''
    send_text = []
    order_data = load_order_data()

    send_text.append('=' * 6)
    for customer in order_data['customers']:
        send_text.append(customer + ' ' + str(order_data['customers'][customer]['code']))
        
        for product in order_data['customers'][customer]['products']:
            send_text.append('{} x {} {}元'.format(product,
                                                  str(order_data['customers'][customer]['products'][product]['num']),
                                                  str(order_data['customers'][customer]['products'][product]['cost'])
                                                  )
                            )
        send_text.append('共' + str(order_data['customers'][customer]['personal_total']) + '元')
        send_text.append('=' * 6)
        
    return send_text

def payment_list():
    '''
    Make a list of who has not paid.
    Return a list of texts to send.
    '''
    send_text = []
    order_data = load_order_data()

    send_text.append('尚 未 付 款')
    send_text.append('- - - - -')
    
    for customer in order_data['customers']:
        
        if order_data['customers'][customer]['has_paid'] == False:
            send_text.append('{} {}元'.format(customer, str(order_data['customers'][customer]['personal_total'])))
        
    return send_text
        
def order_something(M, buyer):                 
    #order is open, customer start to order

    send_text = []
    order_data = load_order_data()
    
    try:
        #get information from the message
        product, num, cost = M.split()[1:]
        num = int(num)
        cost = int(cost)
        if num == 0 or cost == 0:
            raise
        
        try:
            if buyer not in order_data['customers']:
                order_data['max_code'] += 1
                order_data['customers'][buyer] = {'code' : order_data['max_code'],
                                                  'products' : {product : {'num' : num, 'cost' : cost}},
                                                  'has_paid' : False,
                                                  'personal_total' : cost}
            elif product not in order_data['customers'][buyer]['products']:
                order_data['customers'][buyer]['products'][product] = {'num' : num, 'cost' : cost}
                order_data['customers'][buyer]['personal_total'] += cost
            else:
                order_data['customers'][buyer]['products'][product]['num'] += num
                order_data['customers'][buyer]['products'][product]['cost'] += cost
                order_data['customers'][buyer]['personal_total'] += cost
        except:
            print('Something wrong when dumping customer and product data.')
            
        print(buyer, 'check!')
            
        send_text.append('= 點餐成功:) =')
        dump_order_data(order_data)
    except:
        send_text.append('= 輸入錯誤喔割:( =')
        
    return send_text

def send_list(which_list_to_send):
    try:
        if which_list_to_send == 'check':
            return check_list()
        elif which_list_to_send == 'order':
            return order_list()
        elif which_list_to_send =='payment':
            return payment_list()
    except:
        print('Something wrong when trying to send {}_list.'.format(which_list_to_send))


#print('\n'.join(order_list()))
