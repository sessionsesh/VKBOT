import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from user_list import *
from vk_sender.keyboard import *
from schedule import ssender
import datetime
from helpers import week
import helpers
from schedule import academ_parser
from helpers import group_is_right
from weather.weather_parser import *


def send(vk, user_id, msg='Неизвестная команда', atach=None):
    vk.messages.send(
        user_id=user_id,
        attachment=atach,
        random_id=get_random_id(),
        message=msg
    )


# клавиатура в формате json
keyboard = {
    'one_time': False,
    'buttons': [
        [get_button(label='На сегодня', color='positive')],
        [get_button(label='На завтра', color='negative')],
        [get_button(label='На эту неделю', color='primary')],
        [get_button(label='На следующую неделю', color='default')],
        [get_button(label='Какая группа?', color='default')],
        [get_button(label='Какая неделя?', color='default')]

    ]
}

# для других групп/ преподов
keyboard2 = {
    'one_time': True,
    'buttons': [
        [get_button(label='Сегодня', color='positive')],
        [get_button(label='Завтра', color='negative')],
        [get_button(label='Неделя', color='primary')],
        [get_button(label='След', color='default')]
    ]
}

# only_for_testing = open('D:\\Code\\Python\\VKBOT\\folder.txt', 'wb')
users = {}


def main():
    if folder_checker('D:\\Code\\Python\\VKBOT\\folder.txt'):
        users = din('D:\\Code\\Python\\VKBOT\\folder.txt')
    else:
        users = {}
    vk_session = vk_api.VkApi(
        token='0e536a53faa0b8dce9d3e463379aa4d9d5c49b04d5c469d6078c375790cb9bf7eb12d665b67ef349d3e88')
    vk = vk_session.get_api()
    longpol = VkLongPoll(vk_session)
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            hist = vk.messages.getHistory(user_id=event.user_id)
            print(hist['items'][1]['text'])
            if 'Введите вашу группу' in hist['items'][1]['text'] and not user_checker(str(event.user_id),
                                                                                      "D:\\Code\\Python\\VKBOT\\folder.txt"):
                if not (group_is_right(event.text)):
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message='Ошибка в наименовании группы!\n Повторите попытку'
                    )
                    continue
                users[str(event.user_id)] = event.text.upper()
                dout(users, "D:\\Code\\Python\\VKBOT\\folder.txt")
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Ваша группа {}'.format(event.text.upper())
                )
            if not (user_checker(str(event.user_id), "D:\\Code\\Python\\VKBOT\\folder.txt")):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Введите вашу группу: '
                )
                continue
            if 'бот' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='keyboard',
                    keyboard=get_keyboard(keyboard2)
                )
                continue

            if 'сегодня' in event.text.lower() and 'бот' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(helpers.getPattern(hist['items'][2]['text']),
                                            datetime.date.today()),
                )
                continue
            if 'завтра' in event.text.lower() and 'бот' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(helpers.getPattern(hist['items'][2]['text']),
                                            datetime.date.today() + datetime.timedelta(days=1))
                )
                continue
            if 'неделя' in event.text.lower() and 'бот' in hist['items'][2]['text']:

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisweek(
                        helpers.getPattern(hist['items'][2]['text']),
                                           datetime.date.today()+ datetime.timedelta(weeks = 1))
                    )

                continue
            if 'след' in event.text.lower() and 'бот' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisweek(
                        helpers.getPattern(hist['items'][2]['text']),
                        datetime.date.today() + datetime.timedelta(weeks=2))
                )

                continue
            if event.text.lower() == 'расписание':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Конкретнее...\nВыбери из меню ;)',
                    keyboard=get_keyboard(keyboard)
                )
                continue
            if 'сегодня' in event.text.lower() and 'погода' in hist['items'][2]['text'].lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    attachment=today_photo(vk_session),
                    message=today()
                )
                continue
            if 'завтра' in event.text.lower() and 'погода' in hist['items'][2]['text'].lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    attachment=today_photo_1(vk_session),
                    message=today1()
                )
                continue
            if 'сегодня' in event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today()
                    ),
                )
                continue
            if 'завтра' in event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today() + datetime.timedelta(days=1)
                    )
                )
                continue
            if 'эту' in event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisweek(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today()
                    )
                )
                continue
            if 'след' in event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisweek(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today() + datetime.timedelta(weeks=1)
                    )
                )
                continue
            if 'Какая неделя?' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=str(week(datetime.date.today()))

                )
                continue
            if 'Какая группа?' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=users[str(event.user_id)]
                )
                continue

            if 'уме' in event.text.lower() or 'можешь' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Доступные команды: "расписание", "привет", "погода", "найти %препод_нейм%"'
                )
                continue

            if 'привет' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Привет, {}!'.format(vk.users.get(user_id=event.user_id)[0]['first_name'])
                )
                continue

            if 'найти' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='keyboard',
                    keyboard=get_keyboard(keyboard2)
                )
            if 'сегодня' in event.text.lower() and 'найти' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=academ_parser.find_academic(
                        academ_parser.normal_academ(hist['items'][2]['text'][6:]),
                        datetime.date.today()),
                )
                continue
            if 'завтра' in event.text.lower() and 'найти' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=academ_parser.find_academic(
                        academ_parser.normal_academ(hist['items'][2]['text'][6:]),
                        datetime.date.today() + datetime.timedelta(days=1)),
                )
                continue
            if 'неделя' in event.text.lower() and 'найти' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=academ_parser.academ_week(
                        academ_parser.normal_academ(hist['items'][2]['text'][6:]),
                        datetime.date.today()),
                )
                continue
            if 'след' in event.text.lower() and 'найти' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=academ_parser.academ_week(
                        academ_parser.normal_academ(hist['items'][3]['text'][6:]),
                        datetime.date.today() + datetime.timedelta(weeks=1)),
                )
                continue
            if 'погода' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='keyboard',
                    keyboard=get_keyboard(keyboard2)
                )
                continue
            if 'неделя' in event.text.lower() and 'погода' in hist['items'][2]['text']:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=wth_five(),
                    attachment=wth_five_photo(vk_session)
                )
                continue
            if 'сейчас' in event.text.lower() and 'погода' in hist['items'][2]['text'].lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    attachment=wth_now_photo(),
                    message=wth_now()
                )
                continue


if __name__ == main():
    main()
