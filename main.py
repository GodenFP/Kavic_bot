from fbchat import Client
from fbchat.models import *
from youtubeSearch import get_url_by_title
#from models import *
import openpyxl
import logging
import shelve
import json
import datetime
import os

#logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.INFO)
sep = '\\'


#shelf to store data
pc = shelve.open('shelf' + sep + 'pic_commands')
fg = shelve.open('shelf' + sep + 'forbidden_groups')
hp = shelve.open('shelf' + sep + 'help')
inf = shelve.open('shelf' + sep + 'information')



dt = datetime.datetime



#subclass a bot
class Kavic_Bot(Client):

    order_open = False
    now_shop = []

    
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        '''self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)'''

        M = message_object.text
        

        #if the message is not empty and was sent in a forbidden group
        if M != None and (thread_id not in fg.keys()):
            
            M = M.lower()
            
            if M.startswith('-a ') or M.startswith('add ') or M.startswith('-s ') or M.startswith('search ') or M.startswith('-d ') or M.startswith('delete '):
                with open('song_list.txt', 'r') as song_list:
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
                        elif M.startswith('-d ') or M.startswith('delete '):
                            l.remove(url)

                with open('song_list.txt', 'w') as song_list:
                    for line in l:
                        song_list.write('\n' + line)
                        
                #num of sent songs
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
                    self.sendLocalFiles('Source' + sep + hp[M.split(' ')[1]], thread_id=thread_id, thread_type=thread_type) 
                    
                else:
                    File = open(r'README.txt', mode = 'r', encoding = 'utf-8')
                    r = File.read()
                    self.send(Message(r), thread_id=thread_id, thread_type=thread_type)
                    File.close()
                    
            #class sheet
            if M.startswith('課表'):
                wb = openpyxl.open('Source' + sep + 'class_sheet.xlsx')
                sheet = wb.worksheets[0]

                num_weekday = ['週 一', '週 二', '週 三', '週 四', '週 五']
                
                if len(M.split()) > 1:
                    wkday = int(M.split()[1]) - 1
                    self.send(Message(num_weekday[wkday] + ' 課 表'), thread_id = thread_id, thread_type = thread_type)
                else:
                    wkday = dt.weekday(dt.now())
                    self.send(Message(u'今 日 課 表'), thread_id = thread_id, thread_type = thread_type)
                
                if wkday < 6:
                
                    for c in range(1, 10):
                        
                        self.send(Message(text = (b'|   ' + sheet[chr(ord('a') + wkday) + str(c)].value.encode() + b'   |')), thread_id=thread_id, thread_type=thread_type)
                        if c == 4:
                            self.send(Message(text = '---午休---'), thread_id=thread_id, thread_type=thread_type)
                else:
                    self.sendRemoteFiles('https://www.google.com/url?sa=i&url=https%3A%2F%2Fmemes.tw%2Fimage%2F1210&psig=AOvVaw3fXLPUvDLlShStESadX5QL&ust=1616410947407000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJDCwJWewe8CFQAAAAAdAAAAABAD', thread_id = thread_id, thread_type = thread_type)
            #send specific pics    
            if M in pc.keys():
                self.sendLocalFiles('Source' + sep + pc[M], thread_id=thread_id, thread_type=thread_type)
                
            #洗頻
            if M == '洗頻攻擊':
                s = ''
                for i in range(1, 100):
                    s += u'這是洗頻攻擊\n\n∑(っ°Д °;)っ\n\n'

                for i in range(1, 10):
                    self.send(Message(s), thread_id = thread_id, thread_type = thread_type)
                        
                self.sendLocalFiles('Source' + sep + pc[M], thread_id=thread_id, thread_type=thread_type)

            
            #點餐
            if M.startswith('o '):

                text_list = M.split()
                #check whether the command format is right or not
                if len(text_list) > 1 :#and len(text_list) < 5:
                    #order commands that only admin can use
                    if author_id == self.uid:
                        if text_list[1] == 'open':
                            self.order_open = True
                            shop_name = M.split(' ', 2)[2]
                    
                            self.send(Message(u'現正訂購 : ' + shop_name), thread_id = thread_id, thread_type = thread_type)
                            self.sendLocalFiles('Source' + sep + 'shop' + sep + pc[shop_name], message = Message(u'品項:'), thread_id = thread_id, thread_type = thread_type)
                            self.send(Message(u'點餐格式 : o <品名+細項> <數量> <價錢>'), thread_id = thread_id, thread_type = thread_type)
                            self.now_shop.append(shop_name)
                        elif text_list[1] == 'total':
                            with open('tem_list.txt', 'rb') as File:
                                l = File.read().split(b'\n')
                                l.sort()
                                print('---order total---')
                                for order in l:
                                    print(order.decode())
                                print('---order total---')
                                
                        elif text_list[1] == 'close':
                            if len(text_list) == 2:
                                try:
                                    self.now_shop.clear()
                                    
                                    with open('tem_list.txt', 'rb') as File:
                                        l = File.read().split(b'\n')
                                        l.sort()
                                    print('---order total---')
                                    for order in l:
                                        print(order.decode())
                                    print('---order total---')
                                    
                                    os.remove('tem_list.txt')
                                except:
                                    print('list has been removed')
                                finally:
                                    self.send(Message(u'關閉點餐...'), thread_id = thread_id, thread_type = thread_type)
                            '''
                            else:
                                self.now_shop.remove(M.split(' ', 2)[2])
                                self.send(Message('已停止訂購' + M.split(' ', 2)[2]), thread_id = thread_id, thread_type = thread_type)
                            '''
                    #order is open, customer start to order
                    elif self.order_open and len(text_list) == 4:
                        try:
                            buyer = (self.fetchUserInfo(author_id))[author_id]
                            product = text_list[1]
                            num = text_list[2]
                            money = text_list[3]

                            print(buyer.first_name)
                        
                            with open('tem_list.txt', 'ab') as File:
                                File.write(' '.join([buyer.first_name, product, num + '份', money + '元', '\n']).encode('utf-8'))
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
                self.send(Message(u'現正訂購:'), thread_id = thread_id, thread_type = thread_type)
                for shop in self.now_shop:
                    self.sendLocalFiles('Source' + sep + 'shop' + sep + pc[shop], message = Message(shop), thread_id = thread_id, thread_type = thread_type)

                    
            #system commands, only admin can use these
            if author_id == self.uid:
                '''
                if M == 'update':
                    
                    pc.close()
                    fg.close()
                    inf.close()
                    hp.close()

                    pc = shelve.open('shelf\\pic_commands')
                    fg = shelve.open('shelf\\forbidden_groups')
                    hp = shelve.open('shelf\\help')
                    inf = shelve.open('shelf\\information')
                    print('updated successful')
                '''
                #stop listening
                if M == 'leave':
                    self.sendLocalFiles('Source' + sep + 'leaving.jpg', message = Message("I'm leaving..."), thread_id = thread_id, thread_type = thread_type)
                    self.stopListening()                            
            
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
client = Kavic_Bot(inf['email'], inf['password'], session_cookies=cookies)
print('----STARTING SUCCEED----')
client.listen()


# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)

#close all shelve obj
pc.close()
fg.close()
inf.close()
hp.close()
    
