from fbchat import Client
from fbchat.models import *
from youtubeSearch import get_url_by_title
from total import *
from models import *
import openpyxl
import logging
import shelve
import json
import datetime
import os
from getpass import getpass



#logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.INFO)
sep = '\\'






dt = datetime.datetime




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

        M = message_object.text
        

        #if the message is not empty and was sent in a forbidden group
        if M != None and (thread_id not in self.fg.keys()) and (author_id not in self.fg.keys()) :
            
            M = M.lower()
            
            if M.startswith('-a ') or M.startswith('add ') or M.startswith('-s ') or M.startswith('search ') or M.startswith('-d ') or M.startswith('delete '):
                with open('list' + sep + 'song_list.txt', 'r') as song_list:
                    l = song_list.read().split('\n')
                
                num = len(l)
                for title in M[M.find(' ') + 1:].split(','):
                    if title.startswith('https://www.youtube.com/'):
                        l.append(title)
                    elif title != '':
                        url = get_url_by_title(title)
                        if M.startswith('-a ') or M.startswith('add '):
                            l.append(url)
                        elif M.startswith('-s ') or M.startswith('search '):
                            self.send(Message(url), thread_id = thread_id, thread_type = thread_type)
                        elif M.startswith('-d ') or M.startswith('delete ') and only_for_admin(self.uid, author_id):
                            l.remove(url)

                with open('list' + sep + 'song_list.txt', 'w', encoding = 'utf-8') as song_list:
                    for line in l:
                        song_list.write(line + '\n')
                        
                #num of sent songs or deleted songs
                if M.startswith('-a ') or M.startswith('add '):
                    self.send(Message(u'You點了 ' + str(len(l) - num) + u' 首song(s) :)'), thread_id = thread_id, thread_type = thread_type)
                if M.startswith('-d ') or M.startswith('delete '):
                    self.send(Message(u'You刪了 ' + str(num - len(l)) + u' 首song(s) :('), thread_id = thread_id, thread_type = thread_type)

                    
            #help message
            if M.startswith('-h') or M.startswith('help'):
                logging.debug('help received')

                #if there's something behind 'help', send something
                if len(M.split(' ')) > 1:
                    print('hi')
                    self.sendLocalFiles('Source' + sep + self.hp[M.split(' ')[1]], thread_id=thread_id, thread_type=thread_type) 
                    
                else:
                    File = open(r'README.txt', mode = 'r', encoding = 'utf-8')
                    r = File.read()
                    self.send(Message(r), thread_id=thread_id, thread_type=thread_type)
                    File.close()
                    
            #class sheet
            if M.startswith('課表'):
                wb = openpyxl.open('Source' + sep + 'class_sheet.xlsx')
                sheet = wb.worksheets[0]

                num_weekday = ('週 一', '週 二', '週 三', '週 四', '週 五', '週六', '週日')
                
                if len(M.split()) > 1:
                    wkday = int(M.split()[1]) - 1
                    self.send(Message(num_weekday[wkday] + ' 課 表'), thread_id = thread_id, thread_type = thread_type)
                else:
                    wkday = dt.weekday(dt.now())
                    self.send(Message(u'今 日 課 表'), thread_id = thread_id, thread_type = thread_type)

                #if the day asked is a normal day, send class sheet
                if wkday < 5:
                
                    for c in range(1, 10):
                        
                        self.send(Message(text = (b'|   ' + sheet[chr(ord('a') + wkday) + str(c)].value.encode() + b'   |')), thread_id=thread_id, thread_type=thread_type)
                        if c == 4:
                            self.send(Message(text = '---午休---'), thread_id=thread_id, thread_type=thread_type)
                else:
                    self.sendLocalFiles('Source' + sep + 'no.png', thread_id = thread_id, thread_type = thread_type)
                    
            #send specific pics    
            if M in self.pc.keys():
                try:
                    self.sendLocalFiles('Source' + sep + self.pc[M], thread_id=thread_id, thread_type=thread_type)
                except:
                    print('pic not found, it\'s ok maybe')
            #洗頻
            if M == '洗頻攻擊' and only_for_admin(self.uid, author_id):
                s = ''
                for i in range(1, 100):
                    s += u'這是洗頻攻擊\n\n∑(っ°Д °;)っ\n\n'

                for i in range(1, 10):
                    self.send(Message(s), thread_id = thread_id, thread_type = thread_type)
                        
                self.sendLocalFiles('Source' + sep + self.pc[M], thread_id=thread_id, thread_type=thread_type)

            
            #點餐
            if M.startswith('o '):

                text_list = M.split()
                #check whether the command format is right or not
                if len(text_list) > 1 :#and len(text_list) < 5:
                    #order commands that only admin can use
                    if only_for_admin(self.uid, author_id):
                        if text_list[1] == 'open':
                            self.order_open = True
                            shop_name = M.split(' ', 2)[2]
                    
                            self.send(Message(u'現正訂購 : ' + shop_name), thread_id = thread_id, thread_type = thread_type)
                            self.sendLocalFiles('Source' + sep + 'shop' + sep + self.pc[shop_name], message = Message(u'品項:'), thread_id = thread_id, thread_type = thread_type)
                            self.send(Message(u'點餐格式 : o <品名+細項> <數量> <價錢>'), thread_id = thread_id, thread_type = thread_type)
                            self.now_shop.append(shop_name)
                            
                        elif text_list[1] == 'total':
                            list_total()
                                
                        elif text_list[1] == 'close':
                            if self.order_open:
                                try:
                                    list_total()
                                    os.remove('list' + sep + 'record_list.txt')
                                except:
                                    print('list has been removed')
                                finally:
                                    self.send(Message(u'關閉點餐...'), thread_id = thread_id, thread_type = thread_type)
                                    self.now_shop.clear()
                                    self.order_open = False
                            else:
                                print('not open yet')
                            '''
                            else:
                                self.now_shop.remove(M.split(' ', 2)[2])
                                self.send(Message('已停止訂購' + M.split(' ', 2)[2]), thread_id = thread_id, thread_type = thread_type)
                            '''
                        elif text_list[1] == 'check':
                            try:
                                with open('list' + sep + 'final_list.txt', encoding = 'utf-8') as fl:
                                    flr = fl.read()
                                    self.send(Message(flr), thread_id = thread_id, thread_type = thread_type)
                            except:
                                print('something wrong when opening the file "final_list.txt"')
                    #order is open, customer start to order
                    elif self.order_open and len(text_list) == 4:
                        try:
                            buyer = (self.fetchUserInfo(author_id))[author_id]
                            product, num, money = text_list[1:]

                            print(buyer.first_name, 'check!')

                            
                            with open('list' + sep + 'record_list.txt', 'a', encoding = 'utf-8') as File:
                                File.write(' '.join([buyer.first_name, product, num + '份', money + '元', '\n']))
                                self.send(Message(u'點餐成功:)'), thread_id = thread_id, thread_type = thread_type)
                        except:
                            self.send(Message(u'輸入錯誤喔割:('), thread_id = thread_id, thread_type = thread_type)
                    #order not open
                    elif not self.order_open:
                        self.send(Message(u'還沒開訂 哥'), thread_id = thread_id, thread_type = thread_type)
                    else:
                        self.send(Message(u'輸入錯誤喔:('), thread_id = thread_id, thread_type = thread_type)
                        
                else:
                    self.send(Message(u'輸入錯誤喔ㄍ:('), thread_id = thread_id, thread_type = thread_type)
                    
            #send menu pic
            if M.startswith('菜單') or M.startswith('menu'):
                if self.order_open:
                    self.send(Message(u'現正訂購:'), thread_id = thread_id, thread_type = thread_type)
                    for shop in self.now_shop:
                        self.sendLocalFiles('Source' + sep + 'shop' + sep + self.pc[shop], message = Message(shop), thread_id = thread_id, thread_type = thread_type)
                else:
                    self.send(Message('not opennnn'), thread_id = thread_id, thread_type = thread_type)

            if only_for_admin(self.uid, author_id): 
            #system commands, only admin can use these
                
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
                    self.sendLocalFiles('Source' + sep + 'leaving.jpg', message = Message("I'm leaving..."), thread_id = thread_id, thread_type = thread_type)
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
    
