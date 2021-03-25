

sep = '\\'

def take_product_name(order):
    return order.split()[1]
    

def list_total():
    with open('list' + sep + 'record_list.txt', encoding = 'utf-8') as rl, open('list' + sep + 'list_for_order.txt', 'w', encoding = 'utf-8') as lfo,\
         open('list' + sep + 'final_list.txt', 'w', encoding = 'utf-8') as fl:
        
        lread = rl.read().split('\n')
        lread.remove('')
        print(lread)
        lread.sort(key = take_product_name)
        ord_dic = {}
        cus_dic = {}
        


        
        for order in lread:
            name, product, num, cost = order.split()
            
            num = int(num[:-1])
            cost = int(cost[:-1])
            if product not in ord_dic.keys():
                ord_dic[product] = [num, cost]
            else:
                ord_dic[product][0] += num
                ord_dic[product][1] += cost

            if name not in cus_dic.keys():
                cus_dic[name] = { product : [num, cost] }
            else:
                if product not in cus_dic[name].keys():
                    cus_dic[name][product] = [num, cost]
                else:
                    cus_dic[name][product][0] += num
                    cus_dic[name][product][1] += cost
            
        for key in ord_dic.keys():
            lfo.write(key + ' ' + str(ord_dic[key][0]) + '份 ' + str(ord_dic[key][1]) + '元' + '\n')

        total = 0
        for key in cus_dic.keys():
            fl.write(key + ':\n')
            personal_total = 0
            for product in cus_dic[key].keys():
                fl.write(' '.join([product, str(cus_dic[key][product][0]) + '份', str(cus_dic[key][product][1]) + '元', '\n']))
                personal_total += cus_dic[key][product][1]
            total += personal_total
            fl.write('共' + str(personal_total) + '元\n-----\n')




    
