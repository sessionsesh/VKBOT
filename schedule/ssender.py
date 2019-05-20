import datetime
from schedule.sparser import *
from helpers import *


def thisday(group, wk_day=datetime.datetime.today().weekday()):  # 0 - понедельник
    if checkPattern(group) != 'mistake in group name.':
        count = 0
        for each in range(len(group_list)):
            if group_list[each] != group.upper():
                count += 1
        if count == len(group_list):
            return 'unknown group'
    else:
        return 'mistake in group name.'
    message = ''
    wk_num = 1  # поменять на функцию определения чётной и нечётной недели
    #  region 0-6
    d = ''
    list = {0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN"}
    for i in list:
        if i == wk_day:
            d = list[i]
            break
    message = 'Расписание на {} \n'.format(datetime.datetime.today())
    for i in range(6):
        count = 0
        subject = groups[group][d][i][wk_num]['subject']
        lesson_type = groups[group][d][i][wk_num]['lesson_type']
        lecturer = groups[group][d][i][wk_num]['lecturer']
        classroom = groups[group][d][i][wk_num]['classroom']
        list = [subject, lesson_type, lecturer, classroom]
        for k in range(len(list)):
            if count == 3:
                for j in range(4):
                    list[j] = ''
            if list[k] == '':
                list[k] = '-'
                count += 1
            elif k != 3:
                list[k] += ','
        message += ('{}){}{}{}{}\n'.format
                    (i + 1,
                     list[0],
                     list[1],
                     list[2],
                     list[3]
                     )
                    )

    if wk_day == 6:
        message = 'Сегодня воскресенье, пар нет.\n'
    # endregion
    return message

print(thisday("ИКБО-10-18"))
