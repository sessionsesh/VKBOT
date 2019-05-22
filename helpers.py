import re
import datetime


#  Четная/нечётная неделя
def wk_cnt(date):
    cur_y = int(date.strftime('%Y'))
    if int(date.strftime('%m')) < 9:
        sep = datetime.date(cur_y, 9, 1) - datetime.timedelta(days=365)
    else:
        sep = datetime.datetime(cur_y, 9, 1)
    day = 0
    weeks = 1
    x = sep + datetime.timedelta(days=day)
    while x != date:
        x = sep + datetime.timedelta(days=day)
        if day % 7 == 0:
            weeks += 1
        day += 1
    if weeks % 2 == 0:
        return True
    else:
        return False


# возвращает понедельник полученной даты
def make_monday(date):
    if date.strftime('%A').lower() != 'monday'.lower():
        date = date - datetime.timedelta(days=int(date.strftime('%w')) - int(1))
    return date


# Подходит ли группа под шаблон
def checkPattern(str):
    pattern = r'^\D\D\D\D-\d\d-\d\d$'
    if re.search(pattern, str):
        return True
    else:
        return False

