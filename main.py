# coding=utf-8
from fbchat import Client
from fbchat.models import *
from _order_func import *
from _simple_func import *
from _song_list_func import song_options
from datetime import datetime as dt
import logging
import json

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.INFO)

with open('Data' + sep + 'pic.json', encoding='utf-8') as js:
    pic = json.load(js)

block_list = ['3051843494915681']
admin_list = ['100064587296661', '100065838080884']


# subclass a bot
class KavicBot(Client):

    # onMessage function
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        """onMessage func
        """

        '''self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        '''
        global pic, block_list
        
        # shorten these for convenience
        message = message_object.text
        tid = thread_id
        ttp = thread_type

        # if the message is not empty and was sent in a forbidden group###
        # if nothing wrong, judge the message###
        
        if message is not None \
                and ((tid not in block_list and author_id not in block_list)
                     or author_id in admin_list):
            
            message = message.lower()

            # song command
            if check_song_related(message):
                for text in song_options(message):
                    self.send(Message(text), tid, ttp)

            if message == '歌單' or message == 'song list':
                self.send(Message('https://www.youtube.com/playlist?list=PLQu61FekieSStFTy3f3YIEvBy7xo2Yqho'), tid, ttp)
            '''
            # will interrupt program
            if message.startswith('song list ') and author_id in admin_list:
                if len(message.split()) > 3:
                    num = int(message.split()[3])
                else:
                    num = 5

                choice = message.split()[2]
                if choice == 'update':
                    update_song_list(num)
                elif choice == 'delete':
                    delete_from_song_list(num)
                elif choice == 'add':
                    add_to_song_list(num)
            '''
            # help message
            if message == '-h' or message == 'help':
                # if there's something behind 'help', send something
                with open('README.txt', mode='r', encoding='utf-8') as File:
                    r_help = File.read()
                    self.send(Message(r_help), tid, ttp)
                                        
            # curriculum
            if message.startswith('課表'):
                if len(message.split()) > 1:
                    day_num = int(message.split()[1]) - 1
                else:
                    day_num = dt.weekday(dt.now())
            
                self.send(Message('\n\n'.join(curriculum(day_num))), tid, ttp)
                    
                if day_num >= 5:
                    self.sendLocalFiles('Data' + sep + 'pic' + sep + 'no.png', None, tid, ttp)
                    
            # send specific pics
            if message in pic:
                try:
                    self.sendLocalFiles('Data' + sep + 'pic' + sep + pic[message], None, tid, ttp)
                except FileNotFoundError:
                    print('Pic not found, it\'s ok maybe.')
            
            # 洗頻
            if message == '洗頻攻擊' and author_id in admin_list:
                text = ''
                for i in range(1, 100):
                    text += '這是洗頻攻擊\n\n∑(っ°Д °;)っ\n\n'

                for i in range(1, 10):
                    self.send(Message(text), tid, ttp)
                        
                self.sendLocalFiles('Data' + sep + 'pic' + sep + pic[message], None, tid, ttp)

# ---------------------------order---------------------------
            # 點餐
            if message.startswith('o '):
                
                try:
                    order_data = load_order_data()
                except FileNotFoundError:
                    # can't find order_data, create a new data json
                    dump_order_data({'customers': {}, 'shops': [], 'order_open': False, 'max_code': 0})
                    order_data = load_order_data()

                # admin command
                if author_id in admin_list:

                    command = message.split()[1]
                    
                    if command == 'open':
                                  
                        shop_name = message.split(' ', 2)[2]
                                  
                        # send order information
                        if shop_name in pic['shop']:
                            self.send(Message('現正訂購 : ' + shop_name), tid, ttp)
                            self.sendLocalFiles('Data' + sep + 'shop' + sep + pic['shop'][shop_name],
                                                Message('品項:'), tid, ttp)
                            self.send(Message('= 200元內酌收5元服務費 =\n= 超過則每200元加收5元 ='), tid, ttp)
                            self.send(Message('= 200元內酌收5元服務費 =\n= 超過則每200元加收5元 ='), tid, ttp)

                        else:
                            self.send(Message('= 沒這家店ㄟ ='), tid, ttp)
                            
                        # remove last json data
                        if not order_data['order_open']:
                            order_data = {'customers': {}, 'shops': [], 'order_open': True, 'max_code': 0}

                        # add shop
                        if shop_name not in order_data['shops']:
                            order_data['shops'].append(shop_name)
                        
                        # dump order data
                        dump_order_data(order_data)
                         
                    elif command == 'close':
                        if order_data['order_open']:
                            order_data['order_open'] = False
                            dump_order_data(order_data)
                            self.send(Message('= 關閉點餐... ='), tid, ttp)
                        else:
                            print('Can\'t close, not open yet.')
                    
                    elif command == 'show':
                        # print order data to check
                        print(json.dumps(order_data, indent=4, ensure_ascii=False))
                    # list: o list which_list
                    elif command == 'list':
                        self.send(Message('\n'.join(order_send_list(message.split()[2]))), tid, ttp)
                    # remove: o rm who what
                    elif command == 'rm' or command == 'remove':
                        self.send(Message('\n'.join(order_remove_item(tuple(message.split()[2:])))), tid, ttp)
                    # search: o search (product_name or code)
                    elif command == 'search':
                        self.send(Message('\n'.join(order_search_something(message.split()[2]))), tid, ttp)
                    # charge: o c charge_who charge_how_much
                    elif command == 'c' or command == 'charge':
                        self.send(Message('\n'.join(order_charge(tuple(message.split()[2:])))), tid, ttp)
                    # modify: o md md_who md_what with_what
                    elif command == 'md' or command == 'modify':
                        self.send(Message('\n'.join(order_modify_item(tuple(message.split()[2:])))), tid, ttp)
                    elif command == 'reset':
                        self.send(Message('\n'.join(order_reset_has_paid(message.split()[2]))), tid, ttp)
                    else:
                        print('= Type wrong =')
# =============================================================================
                elif message.split()[1] == 'help':
                    self.send(Message(u'= 點餐格式 : o <品名+細項> <數量> <價錢> ='), tid, ttp)
                
                elif order_data['order_open']:
                    # order is open, receive order
                    for text in order_something(message, buyer=(self.fetchUserInfo(author_id))[author_id].first_name):
                        self.send(Message(text), tid, ttp)
                # if order not open
                elif not order_data['order_open']:
                    self.send(Message('= 還沒開訂 哥 ='), tid, ttp)
                else:
                    self.send(Message('= 輸入錯誤喔:( ='), tid, ttp)

            # send menu pic
            if message.startswith('菜單') or message.startswith('menu'):
                order_data = load_order_data()
                if order_data['order_open']:
                    self.send(Message('= 現正訂購 ='), tid, ttp)
                    for shop in order_data['shops']:
                        self.sendLocalFiles('Data' + sep + 'shop' + sep + pic['shop'][shop], Message(shop), tid, ttp)
                    self.send(Message('= 200元內酌收5元服務費 =\n= 超過則每200元加收5元 ='), tid, ttp)
                else:
                    self.send(Message('= Not opennnnnnN. ='), tid, ttp)
# ---------------------------order---------------------------
            # system commands, only admin can use these
            if author_id in admin_list:
                # update pic data json
                if message == 'update':
                    with open('Data' + sep + 'pic.json', encoding='utf-8') as js_file:
                        pic = json.load(js_file)
                        
                    print('updated successful')

                # block thread(block until this robot shut down or unblock)
                if message.startswith('block '):
                    block_list.append(message.split()[1])
                    print('{} has been blocked.'.format(message.split()[1]))
                if message.startswith('unblock '):
                    block_list.remove(message.split()[1])
                    print('{} has been unblocked.'.format(message.split()[1]))
                    
                # stop listening
                if message == 'leave':
                    self.sendLocalFiles('Data' + sep + 'pic' + sep + 'leaving.jpg',
                                        Message("= I'm leaving... ="), tid, ttp)
                    self.stopListening()
                    
                
# -----------------------------------------------------------------------
           
# initialize cookies
cookies = {}
try:
    # Load the session cookies
    with open('Data' + sep + 'personal_data' + sep + 'session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    print('Can\'t load sessioin.json.')

# connect bot
try:
    with open('Data' + sep + 'personal_data' + sep + 'facebook.json') as js:
        facebook = json.load(js)
except FileNotFoundError:
    with open('Data' + sep + 'personal_data' + sep + 'facebook.json', 'w') as js:
        facebook = {'email': input('Enter your email:'), 'password': input('Enter your password:')}
        json.dump(facebook, js)
        
client = KavicBot(facebook['email'], facebook['password'], session_cookies=cookies)
print('----STARTING SUCCEED----')
client.listen()


# Save the session again
with open('Data' + sep + 'personal_data' + sep + 'session.json', 'w') as file:
    json.dump(client.getSession(), file)
