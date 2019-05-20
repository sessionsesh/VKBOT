import re
import datetime


#  Четная/нечётная неделя
def week_counter():
    wk_day = datetime.datetime.today().weekday()


# Подходит ли группа под шаблон
def checkPattern(str):
    pattern = r'^\D\D\D\D-\d\d-\d\d$'
    if re.search(pattern, str):
        return True
    else:
        return False
