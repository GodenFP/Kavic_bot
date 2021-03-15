from fbchat import Client
from fbchat.models import *
from youtubeSearch import get_url_by_title
import openpyxl
import logging
import shelve
import json
import datetime
logging.basicConfig(level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logging.disable(logging.CRITICAL)
sh = shelve.open('pic_commands')
dt = datetime.datetime

#subclass a bot
class Kavic_Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        '''self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)'''

        M = message_object.text
        
        if M != None:
            if M.startswith('add ') or M.startswith('-a ') or M.startswith('-s ') or M.startswith('search '):
                song_list = open('song_list.txt', 'a')

                tem_sl = M[M.find(' ') + 1:].split(',')
                
                num = 0
                for title in tem_sl:
                    if title.startswith('https://www.youtube.com/'):
                        song_list.write('\n' + title)
                        num = num + 1
                    else:
                        url = get_url_by_title(title)
                        if M.startswith('add ') or M.startswith('-a '):
                            song_list.write('\n' + url)
                            num = num + 1
                        else:
                            self.send(Message(text = url), thread_id = thread_id, thread_type = thread_type)
                     
                        
                if M.startswith('add ') or M.startswith('-a '):
                    self.send(Message('You submitted ' + str(num) + ' song(s). :))'), thread_id=thread_id, thread_type=thread_type)

            #exclude certain group(s)
            if thread_id != 3051843494915681:

                #help message
                if M.startswith('-h') or M.startswith('help'):
                    File = open(r'README.txt', mode = 'r', encoding = 'utf-8')
                    r = File.read()
                    self.send(Message(text = r), thread_id=thread_id, thread_type=thread_type)
                    File.close()
                    
                #class sheet
                if M.startswith('課表'):
                    wb = openpyxl.open('Source\\class_sheet.xlsx')
                    sheet = wb.worksheets[0]

                    wkday = chr(ord('a') + dt.weekday(dt.now()))

                    self.send(Message(text = u'--今日課表--'), thread_id=thread_id, thread_type=thread_type)
                    for i in range(1, 10):
                        
                        self.send(Message(text = sheet[wkday + str(i)].value.encode()), thread_id=thread_id, thread_type=thread_type)
                        
                    
                
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
client = Kavic_Bot("ak9806753@gmail.com", "ak98564586", session_cookies=cookies)
client.listen()


# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)
    
