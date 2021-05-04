import json
sep = '\\'
# =====================


def check_song_related(message):
    if message.startswith('-a ') or message.startswith('add ') \
        or message.startswith('-s ') or message.startswith('search ') \
            or message.startswith('-d ') or message.startswith('delete '):
        return True
    else:
        return False


def curriculum(day_num):
    with open('Data' + sep + 'curriculum.json', encoding='utf-8') as js:
        course_data = json.load(js)

    send_text = [('= ' + course_data[day_num]['weekday'] + ' 課 表 =').center(20)]
    if day_num < 5:
        for cls_num in range(0, len(course_data[day_num]['courses'])):
            send_text.append(course_data[day_num]['courses'][cls_num].center(20))
            if cls_num == 3:
                send_text.append('- - - 午休 - - - '.center(20))
    return send_text
