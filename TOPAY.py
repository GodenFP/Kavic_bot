from _order_func import payment_list, load_order_data, dump_order_data

with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()
    
command = ''

while command != 'quit':
    command = input('what to do : ')

    if command.startswith('clear'):
        code = int(command.split()[1])
        
        order_data = load_order_data()
        for customer in order_data['customers']:
            if order_data['customers'][customer]['code'] == code:
                order_data['customers'][customer]['has_paid'] = True
                break
                
        dump_order_data(order_data)
        
        print('clear successful!')
        print('=' * 10)
        print('\n'.join(payment_list()))
        print('=' * 10)
    elif command != 'quit':
        print('input error!')
