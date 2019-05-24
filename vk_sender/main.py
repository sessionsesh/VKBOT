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

# для других групп
keyboard2 = {
    'one_time': True,
    'buttons': [
        [get_button(label='На сегодня', color='positive')],
        [get_button(label='На завтра', color='negative')],
        [get_button(label='На эту неделю', color='primary')],
        [get_button(label='На следующую неделю', color='default')]
    ]
}

# only_for_testing = open('D:\\Code\\Python\\VKBOT\\folder.txt', 'wb')
users = {}


def main():
    users = din('D:\\Code\\Python\\VKBOT\\folder.txt')
    vk_session = vk_api.VkApi(
        token='0e536a53faa0b8dce9d3e463379aa4d9d5c49b04d5c469d6078c375790cb9bf7eb12d665b67ef349d3e88')
    vk = vk_session.get_api()
    longpol = VkLongPoll(vk_session)
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if not (user_checker(str(event.user_id), "D:\\Code\\Python\\VKBOT\\folder.txt")):
                flag1 = True
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Введите вашу группу: '
                )
                while flag1:
                    longpol1 = VkLongPoll(vk_session)
                    for event1 in longpol1.listen():
                        if event1.type == VkEventType.MESSAGE_NEW and event1.to_me:
                            users[str(event.user_id)] = event1.text.upper()
                            dout(users, "D:\\Code\\Python\\VKBOT\\folder.txt")
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message='Ваша группа {}'.format(event1.text.upper())
                            )
                            flag1 = False
                            break

            elif event.text.lower() == 'расписание':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Конкретнее...\nВыбери из меню ;)',
                    keyboard=get_keyboard(keyboard)
                )
                continue
            elif 'На сегодня' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today()
                    ),
                )
                continue
            elif 'На завтра' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today() + datetime.timedelta(days=1)
                    )
                )
                continue
            elif 'На эту неделю' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisweek(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today()
                    )
                )
                continue
            elif 'На следующую неделю' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisweek(
                        get_group(event.user_id, "D:\\Code\\Python\\VKBOT\\folder.txt"),
                        datetime.date.today() + datetime.timedelta(weeks=1)
                    )
                )
                continue
            elif 'Какая неделя?' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=str(week(datetime.date.today()))

                )
                continue
            elif 'Какая группа?' == event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=users[str(event.user_id)]
                )
                continue

            elif 'уме' in event.text.lower() or 'можешь' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Много чего :)\nДоступные команды: "расписание", "привет"'
                )
                continue
            elif 'привет' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Привет, {}!'.format(vk.users.get(user_id=event.user_id)[0]['first_name'])
                )
                continue
            elif 'бот' in event.text.lower():
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=ssender.thisday(helpers.getPattern(event.text), datetime.date.today()),
                    keyboard= get_keyboard(keyboard2)
                )
                continue

            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Такой команды нету'
                )
                continue


if __name__ == main():
    main()
