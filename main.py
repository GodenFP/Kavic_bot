from fbchat import Client
from fbchat.models import *
from youtubeSearch import get_url_by_title
import openpyxl
import logging
import shelve
import json
import datetime

#logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.CRITICAL)

#shelf to store data
sh = shelve.open('shelf\\pic_commands')
fg = shelve.open('shelf\\forbidden_groups')
hp = shelve.open('shelf\\help')
inf = shelve.open('shelf\\information')

dt = datetime.datetime

#subclass a bot
class Kavic_Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        '''self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)'''

        M = message_object.text
        M = M.lower()

        #if the message is not empty and in a forbidden group
        if M != None and (thread_id not in fg.keys()):
            if M.startswith('add ') or M.startswith('-a ') or M.startswith('-s ') or M.startswith('search '):
                song_list = open('song_list.txt', 'a')
                
                num = 0
                for title in M[M.find(' ') + 1:].split(','):
                    if title.startswith('https://www.youtube.com/'):
                        song_list.write('\n' + title)
                        num = num + 1
                    else:
                        url = get_url_by_title(title)
                        if M.startswith('add ') or M.startswith('-a '):
                            song_list.write('\n' + url)
                        else:
                            self.send(Message(text = url), thread_id = thread_id, thread_type = thread_type)
                        num = num + 1
                #num of sent songs
                if M.startswith('add ') or M.startswith('-a '):
                    self.send(Message(u'You點了 ' + str(num) + u' 首song(s) :)'), thread_id = thread_id, thread_type = thread_type)
                        
                     
            #help message
            if M.startswith('-h') or M.startswith('help'):
                logging.debug('help received')

                #if there's something behind 'help', send something
                if len(M.split(' ')) > 1:
                    print('hi')
                    self.sendLocalFiles('Source\\' + hp[M.split(' ')[1]], thread_id=thread_id, thread_type=thread_type) 
                    
                else:
                    File = open(r'README.txt', mode = 'r', encoding = 'utf-8')
                    r = File.read()
                    self.send(Message(text = r), thread_id=thread_id, thread_type=thread_type)
                    File.close()
                    
            #class sheet
            if M.startswith('課表'):
                wb = openpyxl.open('Source\\class_sheet.xlsx')
                sheet = wb.worksheets[0]

                wkday = chr(ord('a') + dt.weekday(dt.now()))

                #print class sheet 
                self.send(Message(text = u'今 日 課 表'), thread_id=thread_id, thread_type=thread_type)
                for i in range(1, 10):
                        
                    self.send(Message(text = (b'|   ' + sheet[wkday + str(i)].value.encode() + b'   |')), thread_id=thread_id, thread_type=thread_type)
                    if i == 4:
                        self.send(Message(text = '---午休---'), thread_id=thread_id, thread_type=thread_type)
                                
            #send specific pics    
            if M in sh.keys():
                self.sendLocalFiles('Source\\' + sh[M], thread_id=thread_id, thread_type=thread_type)
                
            #洗頻
            if M == '洗頻攻擊':
                s = ''
                for i in range(1, 100):
                    s += u'這是洗頻攻擊\n\n∑(っ°Д °;)っ\n\n'

                for i in range(1, 10):
                    self.send(Message(s), thread_id = thread_id, thread_type = thread_type)
                        
                self.sendLocalFiles('Source\\' + sh[M], thread_id=thread_id, thread_type=thread_type)

            #stop listening
            if M == 'leave' and author_id == self.uid:
                self.sendLocalFiles('Source\\leaving.jpg', message = Message("I'm leaving..."), thread_id = thread_id, thread_type = thread_type)
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
    
