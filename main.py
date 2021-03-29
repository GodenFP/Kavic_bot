from fbchat import Client
from fbchat.models import *

from total import *
from models import *
from youtubePlaylist import *

import logging
import shelve
import json

import os
from getpass import getpass

#logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.INFO)
sep = '\\'

#subclass a bot
class Kavic_Bot(Client):

    order_open = False
    now_shop = []

    #shelf to store data
    pc = shelve.open('shelf' + sep + 'pic_commands')
    fg = shelve.open('shelf' + sep + 'forbidden_groups')
    hp = shelve.open('shelf' + sep + 'help')
    
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        '''
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        '''

        #shorten these for convenience
        M = message_object.text
        tid = thread_id
        ttp = thread_type

        ###if the message is not empty and was sent in a forbidden group###
        ###if nothing wrong, judge the message###
        
        if M != None and (tid not in self.fg.keys()) and (author_id not in self.fg.keys()) :
            
            M = M.lower()

            #song command
            if check_song_related(M):
                for text in song_options(M):
                    self.send(Message(text), tid, ttp)

            if M == 'song list':
                self.send(Message('https://www.youtube.com/playlist?list=PLQu61FekieSStFTy3f3YIEvBy7xo2Yqho'), tid, ttp)
            
            #help message
            if M.startswith('-h') or M.startswith('help'):
                logging.debug('help received')

                #if there's something behind 'help', send something
                if len(M.split()) > 1:
                    print('hi')
                    self.sendLocalFiles('Source' + sep + self.hp[M.split()[1]], None, tid, ttp) 
                    
                else:
                    with open('README.txt', mode = 'r', encoding = 'utf-8') as File:
                        r_help = File.read()
                        self.send(Message(r_help), tid, ttp)
                    
                    
            #class sheet
            if M.startswith('課表'):
                class_sheet(M, self, tid, ttp)
                    
            #send specific pics    
            if M in self.pc.keys():
                try:
                    self.sendLocalFiles('Source' + sep + self.pc[M], None, tid, ttp)
                except:
                    print('pic not found, it\'s ok maybe')
            
            #洗頻
            if M == '洗頻攻擊' and only_for_admin(self.uid, author_id):
                s = ''
                for i in range(1, 100):
                    s += u'這是洗頻攻擊\n\n∑(っ°Д °;)っ\n\n'

                for i in range(1, 10):
                    self.send(Message(s), tid, ttp)
                        
                self.sendLocalFiles('Source' + sep + self.pc[M], None, tid, ttp)

#---------------------------order---------------------------           
            #點餐
            if M.startswith('o '):
                
                if only_for_admin(self.uid, author_id):

                    command = M.split()[1]
                    
                    if command == 'open':
                        self.order_open = True
                        shop_name = M.split(' ', 2)[2]
                    
                        self.send(Message(u'現正訂購 : ' + shop_name), tid, ttp)
                        self.sendLocalFiles('Source' + sep + 'shop' + sep + self.pc[shop_name], Message('品項:'), tid, ttp)
                        self.send(Message('點餐格式 : o <品名+細項> <數量> <價錢>'), tid, ttp)
                        self.now_shop.append(shop_name)
                         
                    elif command == 'close':
                        if self.order_open:
                            try:
                                list_total()
                                os.remove('list' + sep + 'record_list.txt')
                            except:
                                print('list has been removed')
                            finally:
                                self.send(Message(u'關閉點餐...'), tid, ttp)
                                self.now_shop.clear()
                                self.order_open = False
                        else:
                            print('not open yet')
                            
                    elif command == 'check':
                        try:
                            with open('list' + sep + 'final_list.txt', encoding = 'utf-8') as fl:
                                flr = fl.read()
                                self.send(Message(flr), tid, ttp)
                        except:
                            print('something wrong when opening the file "final_list.txt"')
                            
                    elif command == 'total':
                        list_total()

                    elif command == 'help':
                        self.send(Message(u'點餐格式 : o <品名+細項> <數量> <價錢>'), tid, ttp)
                
                elif self.order_open:
                    #order is open, receive order
                    for_order(M, self, tid, ttp, author_id)

                #if order not open
                elif not self.order_open:
                    self.send(Message(u'還沒開訂 哥'), tid, ttp)
                else:
                    self.send(Message(u'輸入錯誤喔:('), tid, ttp)

            #send menu pic
            if M.startswith('菜單') or M.startswith('menu'):
                if self.order_open:
                    self.send(Message(u'現正訂購:'), tid, ttp)
                
                    for shop in self.now_shop:
                        self.sendLocalFiles('Source' + sep + 'shop' + sep + self.pc[shop], Message(shop), tid, ttp)
                else:
                    self.send(Message('not opennnnnnn'), tid, ttp)
#---------------------------order---------------------------
                
            #system commands, only admin can use these 
            if only_for_admin(self.uid, author_id):

                #update shelf
                if M == 'update':

                    self.pc.close()
                    self.fg.close()
                    self.hp.close()

                    self.pc = shelve.open('shelf' + sep + 'pic_commands')
                    self.fg = shelve.open('shelf' + sep + 'forbidden_groups')
                    self.hp = shelve.open('shelf' + sep +'help')
                    
                    print('updated successful')
                
                #stop listening
                if M == 'leave':
                    self.sendLocalFiles('Source' + sep + 'leaving.jpg', Message("I'm leaving..."), tid, ttp)
                    self.stopListening()
                    
        #for 歐鎮源
        #if author_id == '100042346155061':
            #self.sendLocalFiles('Source' + sep + 'asshole.jpg', thread_id=thread_id, thread_type=thread_type)
                
#-----------------------------------------------------------------------
                
#initialize cookies
cookies = {}
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

#connect bot
client = Kavic_Bot(getpass('Enter email:'), getpass('enter password:'), session_cookies=cookies)
print('----STARTING SUCCEED----')
client.listen()


# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)

#close all shelve obj
client.pc.close()
client.fg.close()
client.hp.close()
    
