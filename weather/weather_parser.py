import requests
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload
import PIL.Image as Image
import os


# api: 819012f85e3fd2b9d0da0e7916b318dc
# перевод
def make_rus(eng):
    eng = eng.lower()
    dic = {'clouds': 'облачно', 'rain': 'дождь', 'clear': 'ясно'}
    return dic[eng]


def wind_type(deg):
    if deg >= 0 and deg < 45:
        return 'север'
    if deg >= 45 and deg < 90:
        return 'северо-восток'
    if deg >= 90 and deg < 135:
        return 'восток'
    if deg >= 135 and deg < 180:
        return 'юго-восток'
    if deg >= 180 and deg < 225:
        return 'юг'
    if deg >= 225 and deg < 270:
        return 'юго-запад'
    if deg >= 270 and deg < 315:
        return 'запад'
    if deg >= 315 and deg < 360:
        return 'северо-запад'
    else:
        return deg


def wth_now():
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'id': 524901, 'units': 'metric', 'lang': 'ru', 'APPID': api}
    )
    info = response.json()
    # print(info)
    msg += 'Погода в Москве: {}\nТемпература: {}℃\nВетер: {} м/c, ' \
           '{}\nДавление: {} мм рт. ст, влажность: {}%\n'.format(
        make_rus(info['weather'][0]['main']),
        info['main']['temp'],
        info['wind']['speed'],
        wind_type(info['wind']['deg']),
        info['main']['pressure'],
        info['main']['humidity']
    )
    return msg


def date_is_today(date):
    x = datetime.date(
        int(date[0:4]),
        int(date[5:7]),
        int(date[8:10]),
        # int(date[11:13]),
        # int(date[14:16]),
        # int(date[17:19])
    )
    if datetime.date.today() == x:
        return True
    return False


# ночь/ утро/ день/ вечер
def time_is(date, type):
    x = datetime.time(
        int(date[11:13]),
        int(date[14:16]),
        int(date[17:19])
    )
    if x >= datetime.time(0, 00, 00) and x < datetime.time(6, 00, 00) and type == 'night':
        return True
    if x >= datetime.time(6, 00, 00) and x < datetime.time(12, 00, 00) and type == 'morning':
        return True
    if x >= datetime.time(12, 00, 00) and x < datetime.time(18, 00, 00) and type == 'day':
        return True
    if x >= datetime.time(18, 00, 00) and x < datetime.time(23, 59, 59) and type == 'evening':
        return True
    return False


# средние значение погоды на 5 дней ночью или днём
def middle(info, type):
    days = [0, 0, 0, 0, 0]
    count = 0
    j = 0
    t = 0
    for i in info['list']:
        if not time_is(i['dt_txt'], type):
            continue
        t += int(i['main']['temp'])
        j += 1
        if j % 2 == 0 and j != 0:
            days[count] = t / 2
            t = 0
            if count < 4:
                count += 1

    return days


def StrToDate(str):
    date = datetime.date(
        int(str[0:4]),
        int(str[5:7]),
        int(str[8:10])
    )
    return date


def wth_five():  # погода на пять дней
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    day_temp = middle(info, 'day')
    night_temp = middle(info, 'evening')
    flag = 0
    first = ''
    last = ''
    for i in info['list']:
        if not date_is_today(i['dt_txt']) and flag == 0:
            first = i['dt_txt']
            flag = 1
        last = i['dt_txt']
    msg += 'Погода в Москве с {} по {}\n'.format(StrToDate(first), StrToDate(last))
    for i in range(5):
        msg += '{}|'.format(day_temp[i])
    msg += 'День\n'
    for i in range(5):
        msg += '{}|'.format(night_temp[i])
    msg += 'Вечер\n'
    return msg


def today():
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    flag1 = True
    flag2 = True
    flag3 = True
    flag4 = True

    for i in info['list']:
        if not (date_is_today(i['dt_txt'])):
            if time_is(i['dt_txt'], 'night') and flag1:
                msg += 'Ночь\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag1 = False
            if time_is(i['dt_txt'], 'morning') and flag2:
                msg += 'Утро\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag2 = False
            if time_is(i['dt_txt'], 'day') and flag3:
                msg += 'День\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag3 = False
            if time_is(i['dt_txt'], 'evening') and flag4:
                msg += 'Вечер\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag4 = False
    return msg


def today1():
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    flag1 = True
    flag2 = True
    flag3 = True
    flag4 = True
    f = False
    count = 0
    for i in info['list']:
        if not (date_is_today(i['dt_txt'])) and f:
            if time_is(i['dt_txt'], 'night') and flag1:
                msg += 'Ночь\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag1 = False
            if time_is(i['dt_txt'], 'morning') and flag2:
                msg += 'Утро\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag2 = False
            if time_is(i['dt_txt'], 'day') and flag3:
                msg += 'День\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag3 = False
            if time_is(i['dt_txt'], 'evening') and flag4:
                msg += 'Вечер\nПогода:{}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n\n'.format(
                    make_rus(i['weather'][0]['main']),
                    i['main']['temp'],
                    i['wind']['speed'],
                    wind_type(i['wind']['deg']),
                    i['main']['pressure'],
                    i['main']['humidity']
                )
                flag4 = False
        count += 1
        if count == 7:
            f = True
    return msg


def today_photo_1(vk_sesh):
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    flag1 = True
    flag2 = True
    flag3 = True
    flag4 = True
    f = False
    count = 0
    for i in info['list']:
        if not (date_is_today(i['dt_txt'])) and f:
            if time_is(i['dt_txt'], 'night') and flag1:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis3\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag1 = False
                continue

            if time_is(i['dt_txt'], 'morning') and flag2:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis3\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag2 = False
                continue
            if time_is(i['dt_txt'], 'day') and flag3:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis3\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag3 = False
                continue
            if time_is(i['dt_txt'], 'evening') and flag4:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis3\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag4 = False
                continue
        count += 1
        if count == 7:
            f = True
    img = Image.new('RGB', (200, 50))
    x = 0
    for file in os.listdir("D:\\Code\\Python\\VKBOT\\pcis3"):
        if file.endswith(".png"):
            imga = Image.open(os.path.join("D:\\Code\\Python\\VKBOT\\pcis3", file))
            img.paste(imga, (x, 0))
            x += 50
    img.save('D:\\Code\\Python\\VKBOT\\pcis3\\img.png')
    upload = VkUpload(vk_sesh)
    photo = upload.photo_messages(photos='D:\\Code\\Python\\VKBOT\\pcis3\\img.png')[0]
    return 'photo{}_{}'.format(photo['owner_id'], photo['id'])


def today_photo(vk_sesh):
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    flag1 = True
    flag2 = True
    flag3 = True
    flag4 = True
    for i in info['list']:
        if not (date_is_today(i['dt_txt'])):
            if time_is(i['dt_txt'], 'night') and flag1:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis2\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag1 = False
                continue

            if time_is(i['dt_txt'], 'morning') and flag2:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis2\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag2 = False
                continue
            if time_is(i['dt_txt'], 'day') and flag3:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis2\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag3 = False
                continue
            if time_is(i['dt_txt'], 'evening') and flag4:
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']))
                with open('D:\\Code\\Python\\VKBOT\\pcis2\\{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
                flag4 = False
                continue

    img = Image.new('RGB', (200, 50))
    x = 0
    for file in os.listdir("D:\\Code\\Python\\VKBOT\\pcis2"):
        if file.endswith(".png"):
            imga = Image.open(os.path.join("D:\\Code\\Python\\VKBOT\\pcis2", file))
            img.paste(imga, (x, 0))
            x += 50
    img.save('D:\\Code\\Python\\VKBOT\\pcis2\\img.png')
    upload = VkUpload(vk_sesh)
    photo = upload.photo_messages(photos='D:\\Code\\Python\\VKBOT\\pcis2\\img.png')[0]
    return 'photo{}_{}'.format(photo['owner_id'], photo['id'])


def wth_now_photo(vk_sesh):
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    image = requests.get('http://openweathermap.org/img/w/{}.png'.format(info['weather'][0]['icon']))
    with open('{}.png'.format(info['weather'][0]['icon']), 'wb') as f:
        f.write(image.content)
    upload = VkUpload(vk_sesh)
    photo = upload.photo_messages(photos='{}.png'.format(info['weather'][0]['icon']))[0]
    return 'photo{}_{}'.format(photo['owner_id'], photo['id'])


def wth_five_photo(vk_sesh):
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    attach = []
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': 524901, 'units': 'metric', 'APPID': api}
    )
    info = response.json()
    print(info)
    count = 0
    for i in info['list']:
        if not (date_is_today(i['dt_txt'])):
            if count == 7:
                count = 0
                image = requests.get('http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon']),
                                     stream=True)
                with open('{}.png'.format(i['weather'][0]['icon']), 'wb') as f:
                    f.write(image.content)
            count += 1
    img = Image.new('RGB', (200, 50))
    x = 0
    for file in os.listdir("D:\\Code\\Python\\VKBOT\\vk_sender"):
        if file.endswith(".png"):
            imga = Image.open(os.path.join("D:\\Code\\Python\\VKBOT\\vk_sender", file))
            img.paste(imga, (x, 0))
            x += 50
    img.save('img.png')
    upload = VkUpload(vk_sesh)
    photo = upload.photo_messages(photos='D:\\Code\\Python\\VKBOT\\vk_sender\\img.png')[0]
    attach.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    return attach


print(wth_five())
