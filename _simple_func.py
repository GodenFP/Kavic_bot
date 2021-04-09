from _song_list_func import get_url_by_title
import openpyxl
from datetime import datetime as dt
import json

with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()

#=====================


def only_for_admin(admin_id, author_id):
    if admin_id == author_id:
        return True
    else:
        return False


def load_order_data():
    try:
        with open('Data' + sep + 'order_data.json', encoding = 'utf-8') as js:
            return json.load(js)     
    except:
        print('Can\'t load order_data.')

def dump_order_data(data):
    try:
        with open('Data' + sep + 'order_data.json', 'w', encoding = 'utf-8') as js:
            json.dump(data, js)     
    except:
        print('Can\'t dump order_data.')
        
def check_song_related(M):
    if M.startswith('-a ') or M.startswith('add ') or M.startswith('-s ') or M.startswith('search ') or\
       M.startswith('-d ') or M.startswith('delete '):
        return True
    else:
        return False

    
def song_options(M):
    with open('Data' + sep + 'song_list.txt', 'r') as song_list:
        l = song_list.read().split('\n')
        send_text = []
            
    num = len(l)
    for title in M[M.find(' ') + 1:].split(','):
        if title.startswith('https://www.youtube.com/'):
            if 'list' in title:
                send_text.append('這是list喔:(')
                return send_text
            if title in l:
                send_text.append('U人點過囉!')
                return send_text
            l.append(title)
        elif title != '':
            url = get_url_by_title(title)
            if url in l:
                send_text.append('U人點過囉!')
                return send_text
            
            if M.startswith('-a ') or M.startswith('add '):
                l.append(url)
            elif M.startswith('-s ') or M.startswith('search '):
                text.append(url)
            elif M.startswith('-d ') or M.startswith('delete '):
                l.remove(url)

    with open('Data' + sep + 'song_list.txt', 'w', encoding = 'utf-8') as song_list:
        for line in l:
            if line != '':
                song_list.write(line + '\n')
                        
    #num of sent songs or deleted songs
    if M.startswith('-a ') or M.startswith('add '):
        send_text.append('You點了 ' + str(len(l) - num) + u' 首song(s) :)')
    if M.startswith('-d ') or M.startswith('delete '):
        send_text.append('You刪了 ' + str(num - len(l)) + u' 首song(s) :(')
        
    #retun text list to send
    return send_text

def class_sheet(wkday):
    wb = openpyxl.open('Data' + sep + 'class_sheet.xlsx')
    sheet = wb.worksheets[0]
    send_text = []
    weekday = ('週 一', '週 二', '週 三', '週 四', '週 五', '週 六', '週 日')

    #if the day asked is a normal day, send class sheet
    send_text.append(('= ' + weekday[wkday] + ' 課 表 =').center(20))
    if wkday < 5:   
        for cls in range(1, 10):   
            send_text.append(('||    ' + sheet[chr(ord('a') + wkday) + str(cls)].value + '    ||').center(20))
            if cls == 4:
                send_text.append('- - - 午休 - - - '.center(20))
    return send_text

        
def order_something(M, buyer):                 
    #order is open, customer start to order

    send_text = []
    order_data = load_order_data()
    
    try:
        #get information from the message
        product, num, cost = M.split()[1:]
        try:
            if buyer not in order_data['customers']:
                order_data['customers'][buyer] = {'code' : len(order_data['customers']) + 1,
                                                  'products' : {product : {'num' : int(num), 'cost' : int(cost)}},
                                                  'has_paid' : False,
                                                  'personal_total' : int(cost)}
            elif product not in order_data['customers'][buyer]['products']:
                order_data['customers'][buyer]['products'][product] = {'num' : int(num), 'cost' : int(cost)}
                order_data['customers'][buyer]['personal_total'] += int(cost)
            else:
                order_data['customers'][buyer]['products'][product]['num'] += int(num)
                order_data['customers'][buyer]['products'][product]['cost'] += int(cost)
                order_data['customers'][buyer]['personal_total'] += int(cost)

            if product not in order_data['products']:
                order_data['products'][product] = {'num' : int(num), 'cost' : int(cost)}
            else:
                order_data['products'][product]['num'] += int(num)
                order_data['products'][product]['cost'] += int(cost)
        except:
            print('Something wrong when dumping customer and product data.')
            
        print(buyer, 'check!')
            
        send_text.append('點餐成功:)')
        dump_order_data(order_data)
    except:
        send_text.append('輸入錯誤喔割:(')
        
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
                    
