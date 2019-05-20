import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from user_list import *
from helpers import *


def main():
    users = {}
    vk_session = vk_api.VkApi(
        token='0e536a53faa0b8dce9d3e463379aa4d9d5c49b04d5c469d6078c375790cb9bf7eb12d665b67ef349d3e88')
    vk = vk_session.get_api()
    longpol = VkLongPoll(vk_session)
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if not(user_checker(str(event.user_id),"D:\\Code\\Python\\VKBOT\\folder.txt")):
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
                            flag1 =False
                            break

            if event.text == 'xyz':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='zyx'
                )


if __name__ == main():
    main()
