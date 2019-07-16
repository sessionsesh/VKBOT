import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import PIL.Image as Image
from vk_sender.keyboard import *



def main():
    vk_session = vk_api.VkApi(
        token='0e536a53faa0b8dce9d3e463379aa4d9d5c49b04d5c469d6078c375790cb9bf7eb12d665b67ef349d3e88')
    vk = vk_session.get_api()
    longpol = VkLongPoll(vk_session)
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            #vk.messages.deleteConversation(user_id=event.user_id)
            if event.text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='check output'
                )


if __name__ == main():
    main()
