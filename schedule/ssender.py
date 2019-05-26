import datetime
from schedule.sparser import *
from helpers import *

# расписание на определенный день недели
def thisday(group, date):  # 0 1 2 3 4 5 6
    wk_day = date.weekday()
    if wk_day == 6:
        return 'fuck off! Today is sunday'
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
    if week(date) % 2 == 0:
        wk_num = 1
    else:
        wk_num = 0
    #  region 0-6
    d = ''
    list = {0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN"}
    for i in list:
        if i == wk_day:
            d = list[i]
            break
    message = 'Расписание на {} \n'.format(date.strftime('%d-%m-%Y'))
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

# расписание на вю неделю
def thisweek(group, date):
    message = ''
    mon = make_monday(date)
    for i in range(6):  # 0 1 2 3 4 5 6
        message += thisday(group ,mon + datetime.timedelta(days = i)) +'\n'
    return message

#print(thisweek('ИКБО-10-18', datetime.date.today()))
