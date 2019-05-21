import re
import datetime


#  Четная/нечётная неделя
def week_counter():
    wk_day = datetime.datetime.today().weekday()

# возвращает понедельник полученной даты
def make_monday(date):
    if date.strftime('%A').lower() != 'monday'.lower():
        date = date - datetime.timedelta(days = int(date.strftime('%w')) - int(1))
    return date


# Подходит ли группа под шаблон
def checkPattern(str):
    pattern = r'^\D\D\D\D-\d\d-\d\d$'
    if re.search(pattern, str):
        return True
    else:
        return False
