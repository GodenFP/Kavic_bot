import openpyxl
from datetime import datetime as dt


with open('sep.txt', encoding = 'utf-8') as file:
    sep = file.read()

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
                    
