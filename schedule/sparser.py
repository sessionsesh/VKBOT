import requests
from bs4 import BeautifulSoup
import xlrd

# region чтение xlsx файла с сайта
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
groups = {}
group_list = []
week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
for col_index in range(num_cols):
    group_cell = str(sheet.cell(1, col_index).value)
    # print(group_cell)
    if "-18" in group_cell:
        # group_list.append(group_cell)
        week = {'MON': None, 'TUE': None, 'WED': None, 'THU': None, 'FRI': None, 'SAT': None}
        for k in range(6):
            day = [[], [], [], [], [], []]
            for i in range(6):
                for j in range(2):
                    subject = sheet.cell(3 + j + i * 2 + k * 12, col_index).value
                    lesson_type = sheet.cell(3 + j + i * 2 + k * 12, col_index + 1).value
                    lecturer = sheet.cell(3 + j + i * 2 + k * 12, col_index + 2).value
                    classroom = sheet.cell(3 + j + i * 2 + k * 12, col_index + 3).value
                    lesson = {'subject': subject, 'lesson_type': lesson_type,
                              'lecturer': lecturer, 'classroom': classroom}
                    day[i].append(lesson)
            week[week_days[k]] = day
            groups.update({group_cell: week})
            group_list.append(group_cell)


book = xlrd.open_workbook('D:\\Code\\Python\\VKBOT\\schedule\\schedule2k.xlsx')
sheet = book.sheet_by_index(0)

num_cols = sheet.ncols  # столбцы
num_rows = sheet.nrows  # строки
for col_index in range(num_cols):
    group_cell = str(sheet.cell(1, col_index).value)
    # print(group_cell)
    if "-17" in group_cell:
        # group_list.append(group_cell)
        week = {'MON': None, 'TUE': None, 'WED': None, 'THU': None, 'FRI': None, 'SAT': None}
        for k in range(6):
            day = [[], [], [], [], [], []]
            for i in range(6):
                for j in range(2):
                    subject = sheet.cell(3 + j + i * 2 + k * 12, col_index).value
                    lesson_type = sheet.cell(3 + j + i * 2 + k * 12, col_index + 1).value
                    lecturer = sheet.cell(3 + j + i * 2 + k * 12, col_index + 2).value
                    classroom = sheet.cell(3 + j + i * 2 + k * 12, col_index + 3).value
                    lesson = {'subject': subject, 'lesson_type': lesson_type,
                              'lecturer': lecturer, 'classroom': classroom}
                    day[i].append(lesson)
            week[week_days[k]] = day
            groups.update({group_cell: week})
            group_list.append(group_cell)


book = xlrd.open_workbook('D:\\Code\\Python\\VKBOT\\schedule\\schedule3k.xlsx')
sheet = book.sheet_by_index(0)

num_cols = sheet.ncols  # столбцы
num_rows = sheet.nrows  # строки
for col_index in range(num_cols):
    group_cell = str(sheet.cell(1, col_index).value)
    # print(group_cell)
    if "-16" in group_cell:
        # group_list.append(group_cell)
        week = {'MON': None, 'TUE': None, 'WED': None, 'THU': None, 'FRI': None, 'SAT': None}
        for k in range(6):
            day = [[], [], [], [], [], []]
            for i in range(6):
                for j in range(2):
                    subject = sheet.cell(3 + j + i * 2 + k * 12, col_index).value
                    lesson_type = sheet.cell(3 + j + i * 2 + k * 12, col_index + 1).value
                    lecturer = sheet.cell(3 + j + i * 2 + k * 12, col_index + 2).value
                    classroom = sheet.cell(3 + j + i * 2 + k * 12, col_index + 3).value
                    lesson = {'subject': subject, 'lesson_type': lesson_type,
                              'lecturer': lecturer, 'classroom': classroom}
                    day[i].append(lesson)
            week[week_days[k]] = day
            groups.update({group_cell: week})
            group_list.append(group_cell)
# endregion
print(groups)

def group_checker(group):
    for each in group_list:
        if group.lower() == each.lower():
            return True
    return False
