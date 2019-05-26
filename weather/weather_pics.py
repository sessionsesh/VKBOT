import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload
import PIL.Image as Image
from vk_sender.keyboard import *


def send(vk,user_id, msg='Неизвестная команда', atach=None):
    vk.messages.send(
        user_id=user_id,
        attachment=atach,
        random_id=get_random_id(),
        message=msg
    )



def main():
    vk_session = vk_api.VkApi(
        token='0e536a53faa0b8dce9d3e463379aa4d9d5c49b04d5c469d6078c375790cb9bf7eb12d665b67ef349d3e88')
    vk = vk_session.get_api()

    upload = VkUpload(vk_session)
    attachments = []
    image = requests.get('http://openweathermap.org/img/w/02d.png', stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    print(attachments)
    # -181735299 456239056
    longpol = VkLongPoll(vk_session)
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send(event.user_id, vk, 'att', attachments)


if __name__ == main():
    main()
