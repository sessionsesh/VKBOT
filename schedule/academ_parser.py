import requests
from bs4 import BeautifulSoup
import xlrd
import helpers
import datetime

page = requests.get('https://www.mirea.ru/education/schedule-main/schedule/')
soup = BeautifulSoup(page.text, 'html.parser')
result = soup.find('div', {'id': 'toggle-3'}).findAll('a', {'class': 'xls'})

for x in result:
    if 'IIT' in str(x) and '1k' in str(x) and not ("Zach" in str(x)):
        f = open('schedule1k.xlsx', 'wb')
        y = requests.get(x['href'])
        f.write(y.content)
    if 'IIT' in str(x) and '2k' in str(x) and not ("Zach" in str(x)):
        f = open('schedule2k.xlsx', 'wb')
        y = requests.get(x['href'])
        f.write(y.content)
    if 'IIT' in str(x) and '3k' in str(x) and not ("Zach" in str(x)):
        f = open('schedule3k.xlsx', 'wb')
        y = requests.get(x['href'])
        f.write(y.content)

book = xlrd.open_workbook('D:\\Code\\Python\\VKBOT\\schedule\\schedule1k.xlsx')
sheet = book.sheet_by_index(0)

num_cols = sheet.ncols  # столбцы
num_rows = sheet.nrows  # строки

# print(sheet.cell(1, 1).value)


academics = []
aca_sch = {}
week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
dict = {0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN"}
for col_index in range(num_cols):
    aca_cell = sheet.cell(2, col_index).value
    if "ФИО" in aca_cell:
        for f in range(3, 76):
            if sheet.cell(f, col_index).value != '':
                if not (sheet.cell(f, col_index).value in academics):
                    academics.append(sheet.cell(f, col_index).value)

        for each in academics:
            week = {'MON': None, 'TUE': None, 'WED': None, 'THU': None, 'FRI': None, 'SAT': None}
            aca_sch[each] = week
        for each in academics:
            for w in range(6):
                day = [[{}, {}], [{}, {}], [{}, {}], [{}, {}], [{}, {}], [{}, {}]]
                aca_sch[each][dict[w]] = day

for col_index in range(num_cols):
    aca_cell = sheet.cell(2, col_index).value
    if "ФИО" in aca_cell:
        for i in range(6):
            for j in range(6):
                for k in range(2):
                    if sheet.cell(3 + k + j * 2 + i * 12, col_index).value:
                        subject = sheet.cell(3 + k + j * 2 + i * 12, col_index - 2).value
                        lesson_type = sheet.cell(3 + k + j * 2 + i * 12, col_index - 1).value
                        classroom = sheet.cell(3 + k + j * 2 + i * 12, col_index + 1).value
                        lesson = {'subject': subject, 'lesson_type': lesson_type,
                                  'classroom': classroom}
                        aca_sch[sheet.cell(3 + k + j * 2 + i * 12, col_index).value][dict[i]][j][k].update(lesson)


def check_acadeimc(name):
    for each in academics:
        if name.lower() in each.lower():
            return True
    return False


def normal_academ(name):
    for each in academics:
        if name.lower() in each.lower():
            return str(each)
    print("can't normal")
    return "can't normal"


def find_academic(name, date):
    if not (check_acadeimc(name)):
        return 'academic name mistake'
    wk_day = date.weekday()
    if wk_day == 6:
        return "today is sunday"
    message = ''
    if helpers.week(date) % 2 == 0:
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
    message = 'Расписание {} на {} \n'.format(normal_academ(name), date.strftime('%d-%m-%Y'))
    for i in range(6):
        if len(aca_sch[normal_academ(name)][d][i][wk_num]):
            subject = aca_sch[normal_academ(name)][d][i][wk_num]['subject']
            lesson_type = aca_sch[normal_academ(name)][d][i][wk_num]['lesson_type']
            classroom = aca_sch[normal_academ(name)][d][i][wk_num]['classroom']
        else:
            subject = '-'
            lesson_type = '-'
            classroom = '-'
        listu = [subject, lesson_type, classroom]
        message += ('{}) {},{},{}\n'.format(i+1,listu[0],listu[1],listu[2]))
        if wk_day == 6:
            message = 'Сегодня воскресенье, пар нет.\n'
            # endregion


    return message

def academ_counter(name):
    count = 0
    for each in academics:
        if name.lower() in each.lower():
            count+=1
        if count > 1:
            return False
    return True

def academ_week(name,date):
    msg = ''
    mon = helpers.make_monday(date)
    if not check_acadeimc(name):
        return 'academ name mistake'
    for i in range(6):  # 0 1 2 3 4 5 6
        msg += find_academic(name, mon + datetime.timedelta(days=i)) + '\n'
    return msg
# print(aca_sch[normal_academ('Сафрон')][dict[0]])

#print(find_academic(normal_academ('Сафрон'), datetime.date(2019,5,20)))
#print(aca_sch)

academ_counter('Белова')