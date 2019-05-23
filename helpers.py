import re
import datetime


#  Четная/нечётная неделя
def week(date):
    bsc = (6, 35)
    cur_wk = int(date.strftime('%V'))
    wk = cur_wk - bsc[int(date.month) >= 8]
    return wk


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

def getPattern(str):
    pattern = r'\D\D\D\D-\d\d-\d\d'
    if re.search(pattern, str):
        return re.search(pattern, str)[0].upper()
    else:
        return 'mistake'


