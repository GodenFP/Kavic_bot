from fbchat import Client
from fbchat.models import *

from _order_func import *
from _simple_func import *
from _song_list_func import song_options

import logging
import json

#logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.INFO)

with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()

with open('Data' + sep + 'pic.json', encoding = 'utf-8') as js:
    pic = json.load(js)

block_list = ['3051843494915681']

#subclass a bot
class Kavic_Bot(Client):

    ###onMessage function
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        '''
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        '''
        global pic, block_list
        
        #shorten these for convenience
        M = message_object.text
        tid = thread_id
        ttp = thread_type

        ###if the message is not empty and was sent in a forbidden group###
        ###if nothing wrong, judge the message###
        
        if M != None and ((tid not in block_list and author_id not in block_list) or only_for_admin(self.uid, author_id)):
            
            M = M.lower()

            ###song command
            if check_song_related(M):
                for text in song_options(M):
                    self.send(Message(text), tid, ttp)

            if M == '歌單' or M == 'song list':
                self.send(Message('https://www.youtube.com/playlist?list=PLQu61FekieSStFTy3f3YIEvBy7xo2Yqho'), tid, ttp)
            '''
            #will interrupt program
            if M.startswith('song list ') and only_for_admin(self.uid, author_id):
                if len(M.split()) > 3:
                    num = int(M.split()[3])
                else:
                    num = 5

                choice = M.split()[2]
                if choice == 'update':
                    update_song_list(num)
                elif choice == 'delete':
                    delete_from_song_list(num)
                elif choice == 'add':
                    add_to_song_list(num)
            '''
            ###help message
            if M == '-h' or M == 'help':
                #if there's something behind 'help', send something
                with open('README.txt', mode = 'r', encoding = 'utf-8') as File:
                    r_help = File.read()
                    self.send(Message(r_help), tid, ttp)
                                        
            ###class sheet
            if M.startswith('課表'):
                if len(M.split()) > 1:
                    wkday = int(M.split()[1]) - 1
                else:
                    wkday = dt.weekday(dt.now())
            
                self.send(Message('\n\n'.join(class_sheet(wkday))), tid, ttp)
                    
                if wkday >= 5:
                    self.sendLocalFiles('Data' + sep + 'pic' + sep + 'no.png', None, tid, ttp)
                    
            ###send specific pics    
            if M in pic:
                try:
                    self.sendLocalFiles('Data' + sep + 'pic' + sep + pic[M], None, tid, ttp)
                except:
                    print('Pic not found, it\'s ok maybe.')
            
            ###洗頻
            if M == '洗頻攻擊' and only_for_admin(self.uid, author_id):
                text = ''
                for i in range(1, 100):
                    text += '這是洗頻攻擊\n\n∑(っ°Д °;)っ\n\n'

                for i in range(1, 10):
                    self.send(Message(text), tid, ttp)
                        
                self.sendLocalFiles('Data' + sep + 'pic' + sep + pic[M], None, tid, ttp)

#---------------------------order---------------------------           
            ###點餐
            if M.startswith('o '):
                
                try:
                    order_data = load_order_data()
                except:
                    #can't find order_data, create a new data json
                    dump_order_data({'customers' : {}, 'shops' : [], 'order_open' : False, 'max_code' : 0})
                    order_data = load_order_data()
                        
                if only_for_admin(self.uid, author_id):

                    command = M.split()[1]
                    
                    if command == 'open':
                                  
                        shop_name = M.split(' ', 2)[2]
                                  
                        #send order information
                        if shop_name in pic['shop']:
                            self.send(Message('現正訂購 : ' + shop_name), tid, ttp)
                            self.sendLocalFiles('Data' + sep + 'shop' + sep + pic['shop'][shop_name], Message('品項:'), tid, ttp)
                            self.send(Message('點餐格式 : o <品名+細項> <數量> <價錢>'), tid, ttp)
                        else:
                            self.send(Message('= 沒這家店ㄋㄟ ='), tid, ttp)
                            
                        #remove last json data
                        if order_data['order_open'] == False:
                            order_data = {'customers' : {}, 'shops' : [], 'order_open' : True, 'max_code' : 0}
                            

                        #add shop
                        if shop_name not in order_data['shops']:
                            order_data['shops'].append(shop_name)
                        
                        #dump order data
                        dump_order_data(order_data)
                         
                    elif command == 'close':
                        if order_data['order_open'] == True:
                            
                            order_data['order_open'] = False
                            dump_order_data(order_data)
                                                                                  
                            self.send(Message('= 關閉點餐... ='), tid, ttp)
                                  
                        else:
                            print('Can\'t close, not open yet.')
                    
                    elif command == 'show':
                        #print order data to check
                        print(json.dumps(order_data, indent = 4, ensure_ascii = False))
                        
                    elif command == 'list':
                        self.send(Message('\n'.join(send_list(M.split()[2]))), tid, ttp)
                        
#=============================================================================
                        
                elif M.split()[1] == 'help':
                        self.send(Message(u'點餐格式 : o <品名+細項> <數量> <價錢>'), tid, ttp)
                
                elif order_data['order_open']:
                    #order is open, receive order
                    for text in order_something(M, buyer = (self.fetchUserInfo(author_id))[author_id].first_name):
                        self.send(Message(text), tid, ttp)

                #if order not open
                elif not order_data['order_open']:
                    self.send(Message('還沒開訂 哥'), tid, ttp)
                else:
                    self.send(Message('輸入錯誤喔:('), tid, ttp)

            #send menu pic
            if M.startswith('菜單') or M.startswith('menu'):
                order_data = load_order_data()
                if order_data['order_open']:
                    self.send(Message('= 現正訂購 ='), tid, ttp)
                
                    for shop in order_data['shops']:
                        self.sendLocalFiles('Data' + sep + 'shop' + sep + pic['shop'][shop], Message(shop), tid, ttp)
                else:
                    self.send(Message('Not opennnnnnN.'), tid, ttp)
#---------------------------order---------------------------
                
            ###system commands, only admin can use these 
            if only_for_admin(self.uid, author_id):

                #update pic data json
                if M == 'update':
                    with open('Data' + sep + 'pic.json', encoding = 'utf-8') as js:
                        pic = json.load(js)
                        
                    print('updated successful')

                #block thread(block until this robot shut down or unblock)
                if M == 'block':
                    block_list.append(tid)
                    print('{} has been blocked.'.format(tid))
                if M == 'unblock':
                    block_list.remove(tid)
                    print('{} has been unblocked.'.format(tid))
                    
                #stop listening
                if M == 'leave':
                    self.sendLocalFiles('Data' + sep + 'pic' + sep + 'leaving.jpg', Message("= I'm leaving... ="), tid, ttp)
                    self.stopListening()
                    
                
#-----------------------------------------------------------------------
           
#initialize cookies
cookies = {}
try:
    # Load the session cookies
    with open('Data' + sep + 'personal_data' + sep + 'session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    print('Can\'t load sessioin.json.')

#connect bot
try:
    with open('Data' + sep + 'personal_data' + sep + 'facebook.json') as js:
        facebook = json.load(js)
except:
    with open('Data' + sep + 'personal_data' + sep + 'facebook.json', 'w') as js:
        facebook = {'email' : input('Enter your email:'),
                   'password' : input('Enter your password:')}
        json.dump(facebook, js)
        
client = Kavic_Bot(facebook['email'], facebook['password'], session_cookies = cookies)
print('----STARTING SUCCEED----')
client.listen()


# Save the session again
with open('Data' + sep + 'personal_data' + sep + 'session.json', 'w') as f:
    json.dump(client.getSession(), f)

