from settings import token, group_id, save_path
from qr import QR

import random
import sys
import requests
import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def main():
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, 180619567, wait=25)
    upload_url = vk.photos.getMessagesUploadServer(group_id=group_id)['upload_url']
    qr = QR()

    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
                qr_path, qr_img = qr.createqr(event.obj.text)
                print(qr_path, qr_img)

                # filesd = {'photo': open(qr_path, 'rb')}
                r = requests.post(upload_url,
                                  files={'photo': open(qr_path, 'rb')}).json()

                params = {'server': r['server'],
                          'photo': r['photo'],
                          'hash': r['hash'],
                          'group_id': group_id}
                print(params)
                photo_id = vk.photos.saveMessagesPhoto(**params)[0]['id']

                if event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        random_id=random.randint(1, pow(10, 6)),
                        message="Вот ваш купон",
                        attachment="photo-{}_{}".format(group_id, photo_id)
                    )
                elif event.from_user:
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=random.randint(1, pow(10, 6)),
                        message='Вот ваш купон',
                        attachment="photo-{}_{}".format(group_id, photo_id)
                    )
                # qr.deleteqr(qr_path)
            elif event.type == VkBotEventType.MESSAGE_REPLY:
                print('Новое сообщение-ответ:')
                print('От меня для: ', end='')
                print(event.obj.peer_id)
                print('Текст:', event.obj.text)
                print()
            elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
                print('Печатает ', end='')
                print(event.obj.from_id, end=' ')
                print('для ', end='')
                print(event.obj.to_id)
                print()
            elif event.type == VkBotEventType.GROUP_JOIN:
                print(event.obj.user_id, end=' ')
                print('Вступил в группу!')
                print()
            elif event.type == VkBotEventType.GROUP_LEAVE:
                print(event.obj.user_id, end=' ')
                print('Покинул группу!')
                print()
            else:
                print(event.type)
                print()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()
