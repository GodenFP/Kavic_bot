import json
from _simple_func import sep


def load_order_data():
    try:
        with open('Data' + sep + 'order_data.json', encoding='utf-8') as js:
            return json.load(js)      
    except json.decoder.JSONDecodeError:
        print('Can\'t load order_data.')
    except FileNotFoundError:
        print('Can\'t find order_data when loading.')
        # can't find order_data, create a new data json
        dump_order_data({'customers': {}, 'shops': [], 'order_open': False, 'max_code': 0})
        with open('Data' + sep + 'order_data.json', encoding='utf-8') as js:
            return json.load(js)


def dump_order_data(data):
    try:
        with open('Data' + sep + 'order_data.json', 'w', encoding='utf-8') as js:
            json.dump(data, js, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('Can\'t find order_data when dumping.')


def count_product():
    order_data = load_order_data()
    products = {}

    for customer in order_data['customers']:
        for product in order_data['customers'][customer]['products']:
            product_data = order_data['customers'][customer]['products'][product]
            if product not in products:
                products[product] = {
                        'num': product_data['num'],
                        'cost': product_data['cost']}
            else:
                products[product]['num'] += product_data['num']
                products[product]['cost'] += product_data['cost']
    return products


def order_list():
    """Make a list of products for ordering.
    If more_than_one_shop is True,
    this func will judge the length of product's name.
    Greater than 6, the product will be classified as 'drink',
    otherwise, food(not accurate)
    Return a list of texts to send.
    """
    send_text = []
    total = 0
    products = count_product()
    product_list = list(products.keys())
    more_than_one_shop = (len(load_order_data()['shops']) > 1)

    product_list.sort(key=lambda product_in_product_list: len(product_in_product_list))
    print(product_list)
    for product in product_list:
        if more_than_one_shop and len(product) >= 6:
            send_text.append('共 {} 元\n= = = = ='.format(total))
            total = 0
            more_than_one_shop = False

        send_text.append('{} {}份 {}元\n- - - - -'.format(product,
                                                        str(products[product]['num']), str(products[product]['cost'])))
        total += products[product]['cost']

    send_text.append('共 {} 元'.format(total))
    return send_text


def check_list():
    """Make a list of who ordered, ordered what,
    and how much the personal total is.
    Return a list of texts to send.
    """
    send_text = []
    order_data = load_order_data()

    send_text.append('=' * 6)
    for customer in order_data['customers']:
        send_text.append(customer + ' ' + str(order_data['customers'][customer]['code']))
        personal_total = order_data['customers'][customer]['personal_total']
        fee = (personal_total // 200 + 1) * 5
        for product in order_data['customers'][customer]['products']:
            send_text.append('{} x{} {}元'.format(product,
                                                 str(order_data['customers'][customer]['products'][product]['num']),
                                                 str(order_data['customers'][customer]['products'][product]['cost'])))
        send_text.append('服務費: {}元'.format(fee))
        send_text.append('共' + str(personal_total + fee) + '元')
        send_text.append('=' * 6)
        
    return send_text


def payment_list(display_all=False):
    """Make a list of who has not paid.
    Return a list of texts to send.
    """
    send_text = []
    order_data = load_order_data()
    if not display_all:
        send_text.append('尚 未 付 款')
        send_text.append('- - - - -')
    for customer in order_data['customers']:
        personal_total = order_data['customers'][customer]['personal_total']
        money_has_paid = order_data['customers'][customer]['money_has_paid']
        fee = (personal_total // 200 + 1) * 5
        if display_all:
            send_text.append('{} {}  {}元'.format(str(order_data['customers'][customer]['code']),
                                                 customer,
                                                 str(personal_total + fee)))
        elif money_has_paid != (personal_total + fee):
            send_text.append('{} {}  {}元'.format(str(order_data['customers'][customer]['code']),
                                                 customer,
                                                 str(personal_total + fee - money_has_paid)))
    return send_text


def order_something(message, buyer):
    # order is open, customer start to order

    send_text = []
    order_data = load_order_data()
    
    try:
        # get information from the message
        product, num, cost = message.split()[1:]
        num = int(num)
        cost = int(cost)
        if num == 0 or cost == 0:
            send_text.append('= 數量or金額輸入錯誤 :( =')
            return send_text

        if buyer not in order_data['customers']:
            order_data['max_code'] += 1
            order_data['customers'][buyer] = {'code': order_data['max_code'],
                                              'products': {product: {'num': num, 'cost': cost}},
                                              'money_has_paid': 0,
                                              'personal_total': cost}
        elif product not in order_data['customers'][buyer]['products']:
            order_data['customers'][buyer]['products'][product] = {'num': num, 'cost': cost}
            order_data['customers'][buyer]['personal_total'] += cost
        else:
            order_data['customers'][buyer]['products'][product]['num'] += num
            order_data['customers'][buyer]['products'][product]['cost'] += cost
            order_data['customers'][buyer]['personal_total'] += cost

        print(buyer, 'check!')
        send_text.append('= 點餐成功:) =')
        dump_order_data(order_data)
    except ValueError:
        send_text.append('= 輸入錯誤喔割:( =')
    except KeyError:
        print('json key打錯啦割')
        
    return send_text


def order_send_list(which_list_to_send):
    if which_list_to_send in ('check', 'c'):
        return check_list()
    elif which_list_to_send in ('order', 'o'):
        return order_list()
    elif which_list_to_send in ('payment', 'p'):
        return payment_list()
    elif which_list_to_send in ('payment all', 'pa'):
        return payment_list(True)
    else:
        print('Type wrong list to send!')


# TODO: add docstring and use list
def order_remove_item(remove_who_and_what):
    send_text = []
    order_data = load_order_data()
    try:
        remove_who, remove_what = remove_who_and_what
    except ValueError:
        send_text.append("= 輸入錯誤 =")
        return send_text

    for customer in tuple(order_data['customers'].keys()):
        if remove_who == 'all' or remove_who == str(order_data['customers'][customer]['code']):
            if remove_what == 'all':
                order_data['customers'].pop(customer)
                send_text.append('= 已remove {} 的所有訂單 :( ='.format(customer))
            else:
                for product in tuple(order_data['customers'][customer]['products'].keys()):
                    if remove_what in product:
                        order_data['customers'][customer]['personal_total'] \
                            -= order_data['customers'][customer]['products'][product]['cost']
                        order_data['customers'][customer]['products'].pop(product)
                        if order_data['customers'][customer]['personal_total'] == 0:
                            order_data['customers'].pop(customer)
                        send_text.append('= 已remove {} 的 {} ='.format(customer, product))
            if remove_who != 'all':
                break
    dump_order_data(order_data)
    if len(send_text) == 0:
        send_text.append('= 404 not found :( =')
    return send_text


def order_modify_item(modify_who_and_what_with_what):
    send_text = []
    order_data = load_order_data()
    try:
        modify_who, modify_what, with_what = modify_who_and_what_with_what
    except ValueError:
        send_text.append("= 輸入錯誤 =")
        return send_text

    for customer in tuple(order_data['customers'].keys()):
        if modify_who == 'all' or modify_who == str(order_data['customers'][customer]['code']):
            for product in tuple(order_data['customers'][customer]['products'].keys()):
                if modify_what in product:
                    if with_what not in order_data['customers'][customer]['products']:
                        order_data['customers'][customer]['products'][with_what] = \
                            order_data['customers'][customer]['products'].pop(product)
                    else:
                        original_info = order_data['customers'][customer]['products'].pop(product)
                        order_data['customers'][customer]['products'][with_what]['num'] += original_info['num']
                        order_data['customers'][customer]['products'][with_what]['cost'] += original_info['cost']
                    send_text.append('= 已將 {} 的 {} 更改為 {} ='.format(customer, product, with_what))
            if modify_who != 'all':
                break
    dump_order_data(order_data)
    if len(send_text) == 0:
        send_text.append('= 404 not found :( =')
    return send_text


def order_search_something(something):
    order_data = load_order_data()
    send_text = []
    for customer in order_data['customers']:
        products = order_data['customers'][customer]['products']
        if something == str(order_data['customers'][customer]['code']):
            send_text.append('= = = = =\n{} {}'.format(customer, str(order_data['customers'][customer]['code'])))
            for product in products:
                send_text.append('{} {}份 {}元'.format(product, products[product]['num'], products[product]['cost']))
            send_text.append('= = = = =')
            return send_text
        else:
            for product in products:
                if something in product:
                    send_text.append('{} {}  {} {}份 {}元'.format(str(order_data['customers'][customer]['code']),
                                                                customer,
                                                                product,
                                                                str(products[product]['num']),
                                                                str(products[product]['cost'])))
                    send_text.append('- - - - -')
    if len(send_text) == 0:
        send_text.append('= 404 not found :( =')
    return send_text


# TODO: inspect this F**KIng thing
def order_charge(who_pay_how_much):
    """
    charge: o c who how_much
    """
    send_text = []
    try:
        who, how_much = who_pay_how_much
        if how_much != 'all' and not how_much.isdigit():
            print(how_much)
            send_text.append('= Type Wrong! =')
            return send_text
    except ValueError:
        who = who_pay_how_much[0]
        how_much = 'all'
        
    order_data = load_order_data()
    for customer in order_data['customers']:
        if who == str(order_data['customers'][customer]['code']):
            personal_total = order_data['customers'][customer]['personal_total']
            money_has_paid = order_data['customers'][customer]['money_has_paid']
            if how_much == 'all':
                money_has_paid = personal_total
                send_text.append("= {} 已付清! :) =".format(customer))
            elif how_much.isdigit():
                money_has_paid += int(how_much)
                if money_has_paid == personal_total:
                    send_text.append("= {} 已付清! :) =".format(customer))
                else:
                    send_text.append("= {} 付了 {} 元, 還有 {} 元尚未付清 :) =".format(
                        customer, how_much, str(personal_total - money_has_paid)))
            order_data['customers'][customer]['personal_total'] = personal_total
            order_data['customers'][customer]['money_has_paid'] = money_has_paid
            break
        
    dump_order_data(order_data)
    return send_text


# TODO: is this really needy?
def order_reset_has_paid(code):
    order_data = load_order_data()
    send_text = []
    for customer in order_data['customers']:
        if code == 'all' or int(code) == order_data['customers'][customer]['code']:
            order_data['customers'][customer]['money_has_paid'] = 0
            send_text.append('= {} has been reset! ='.format(customer))
            break
    return send_text
# print('\n'.join(order_pay_money(input().split()[2])))
# print('\n'.join(payment_list()))
