
with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()
product_num_cost = {}
name_product = {}


def take_product_name(order):
    return order.split()[1]
    

def collect_information():
    with open('list' + sep + 'record_list.txt', 'r', encoding = 'utf-8') as rl:
        
        lread = rl.read().split('\n')
        while '' in lread:
            lread.remove('')
        print(lread)
        
        lread.sort(key = take_product_name)
        

        ###collect information and insert them into dicts
        for order in lread:
            name, product, num, cost = order.split()
            
            num = int(num[:-1])
            cost = int(cost[:-1])
            
            if product not in product_num_cost.keys():
                product_num_cost[product] = [num, cost]
            else:
                product_num_cost[product][0] += num
                product_num_cost[product][1] += cost

            if name not in name_product.keys():
                name_product[name] = { product : [num, cost] }
            else:
                if product not in name_product[name].keys():
                    name_product[name][product] = [num, cost]
                else:
                    name_product[name][product][0] += num
                    name_product[name][product][1] += cost

def order_list_for_one_shop():                    
    with open('list' + sep + 'order_list.txt', 'w', encoding = 'utf-8') as order_list:
        total = 0
        for product in product_num_cost.keys():
            total +=product_num_cost[product][1]
            order_list.write(product + ' ' + str(product_num_cost[product][0]) + '份 ' + str(product_num_cost[product][1]) + '元' + '\n')
        order_list.write('共' + str(total) + '元')

def order_list_food_and_drink():
    with open('list' + sep + 'order_list.txt', 'w', encoding = 'utf-8') as order_list:
        drink_list = []
        total_for_food = 0
        total_for_drink = 0
        
        for product in product_num_cost.keys():
            
            if len(product) > 6:
                drink_list.append(product)
            else:
                total_for_food += product_num_cost[product][1]
                order_list.write(product + ' ' + str(product_num_cost[product][0]) + '份 ' + str(product_num_cost[product][1]) + '元' + '\n')
                
        order_list.write('食物共' + str(total_for_food) + '元\n')
        order_list.write('----drink below----\n')
        
        for drink in drink_list:
            total_for_drink += product_num_cost[drink][1]
            order_list.write(drink + ' ' + str(product_num_cost[drink][0]) + '杯 ' + str(product_num_cost[drink][1]) + '元' + '\n')

        order_list.write('飲料共' + str(total_for_drink) + '元')

def who_buy_what_list():
    with open('list' + sep + 'who_buy_what_list.txt', 'w', encoding = 'utf-8') as wbwl:
        code = 0
        
        for name in name_product.keys():
            code += 1
            wbwl.write(str(code) + ' ' + name + '\n')
            personal_total = 0
            for product in name_product[name].keys():
                wbwl.write(' '.join([product, str(name_product[name][product][0]) + '份', str(name_product[name][product][1]) + '元', '\n']))
                personal_total += name_product[name][product][1]
            wbwl.write('共' + str(personal_total) + '元\n-----\n')


def who_order_drink():
    
    with open('list' + sep + 'list_for_order.txt', 'w', encoding = 'utf-8') as lfo:
        for name in name_product.keys():
            for product in name_product[name].keys():
                if len(product) > 6:
                    nl.write(' '.join([key, str(name_product[name][product][0] * 5) + '元', '\n-----\n']))
                    
def who_order_food():

    with open('list' + sep + 'list_for_order.txt', 'w', encoding = 'utf-8') as lfo:
        for name in name_product.keys():
            for product in name_product[name].keys():
                if len(product) <= 6:
                    nl.write(' '.join([key, str(name_product[name][product][0] * 5) + '元', '\n-----\n']))

#-------------------------------------------------

def calc_food_and_drink():
    try:
        collect_information()
    except:
        print('something wrong when collecting order information.')
    order_list_food_and_drink()
    who_buy_what_list()


def calc_only_one_shop():
    try:
        collect_information()
    except:
        print('something wrong when collecting order information.')
    order_list_for_one_shop()
    who_buy_what_list()

