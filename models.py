import fbchat
from fbchat.models import *
from youtubeSearch import get_url_by_title
import openpyxl
import datetime
sep = '\\'
dt = datetime.datetime

#=====================


def only_for_admin(admin_id, author_id):
    if admin_id == author_id:
        return True
    else:
        return False

def check_song_related(M):
    if M.startswith('-a ') or M.startswith('add ') or M.startswith('-s ') or M.startswith('search ') or\
       M.startswith('-d ') or M.startswith('delete '):
        return True
    else:
        return False

    
def song_options(M):
    with open('list' + sep + 'song_list.txt', 'r') as song_list:
        l = song_list.read().split('\n')
        text = []
            
    num = len(l)
    for title in M[M.find(' ') + 1:].split(','):
        if title.startswith('https://www.youtube.com/'):
            l.append(title)
        elif title != '':
            url = get_url_by_title(title)
                
            if M.startswith('-a ') or M.startswith('add '):
                l.append(url)
            elif M.startswith('-s ') or M.startswith('search '):
                text.append(url)
            elif M.startswith('-d ') or M.startswith('delete '):
                l.remove(url)

    with open('list' + sep + 'song_list.txt', 'w', encoding = 'utf-8') as song_list:
        for line in l:
            if line != '':
                song_list.write(line + '\n')
                        
    #num of sent songs or deleted songs
    if M.startswith('-a ') or M.startswith('add '):
        text.append('You點了 ' + str(len(l) - num) + u' 首song(s) :)')
    if M.startswith('-d ') or M.startswith('delete '):
        text.append('You刪了 ' + str(num - len(l)) + u' 首song(s) :(')
        
    #retun text list to send
    return text

def class_sheet(M, client, tid, ttp):
    wb = openpyxl.open('Source' + sep + 'class_sheet.xlsx')
    sheet = wb.worksheets[0]
    text = []
    num_weekday = ('週 一', '週 二', '週 三', '週 四', '週 五', '週 六', '週 日')
                
    if len(M.split()) > 1:
        wkday = int(M.split()[1]) - 1
        text.append(Message(num_weekday[wkday] + ' 課 表'))
    else:
        wkday = dt.weekday(dt.now())
        text.append('今 日 課 表')

    #if the day asked is a normal day, send class sheet
    if wkday < 5:
                
        for cls in range(1, 10):
                        
            text.append(b'|   ' + sheet[chr(ord('a') + wkday) + str(cls)].value.encode() + b'   |')
            if cls == 4:
                text.append('---午休---')
    for t in text:
        client.send(Message(t), tid, ttp)
                
    if wkday >= 5:
        client.sendLocalFiles('Source' + sep + 'no.png', None, tid, ttp)

        
def order_something(M, client, tid, ttp, author_id):             
                                
    #order is open, customer start to order
    try:
        buyer = (client.fetchUserInfo(author_id))[author_id]
        product, num, money = M.split()[1:]

        print(buyer.first_name, 'check!')

                            
        with open('list' + sep + 'record_list.txt', 'a', encoding = 'utf-8') as File:
            File.write(' '.join([buyer.first_name, product, num + '份', money + '元', '\n']))
        client.send(Message('點餐成功:)'), tid, ttp)
    except:
        client.send(Message('輸入錯誤喔割:('), tid, ttp)


                    
