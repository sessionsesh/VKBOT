import requests


# api: 819012f85e3fd2b9d0da0e7916b318dc

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


def wth_today():
    api = '819012f85e3fd2b9d0da0e7916b318dc'
    msg = ''
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'id': 524901, 'units': 'metric', 'lang': 'ru', 'APPID': api}
    )
    info = response.json()
    msg += 'Погода в Москве: {}\nТемпература: {}℃\nВетер: {} м/c, {}\nДавление: {} мм рт. ст, влажность: {}%\n'.format \
            (
            make_rus(info['weather'][0]['main']),
            info['main']['temp'],
            info['wind']['speed'],
            wind_type(info['wind']['deg']),
            info['main']['pressure'],
            info['main']['humidity']
        )
    return msg


print(wth_today())
