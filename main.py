from settings import token, group_id, save_path
from qr import QR
from multiprocessing import Pool, Process, current_process
import random
import requests
import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from jinja2 import Template

index_html = open('static/index.html').read()
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 180619567, wait=25)
upload_url = vk.photos.getMessagesUploadServer(group_id=group_id)['upload_url']


def testing(*args, **kwargs):
    print(args, kwargs)
    return 1 ** 2


def createqr_to_vk(text):
    print('process name: {}'.format(current_process().name))
    qr = QR()
    qr_path, qr_img = qr.createqr(text)
    # print(qr_path, qr_img)

    r = requests.post(upload_url,
                      files={'photo': open(qr_path, 'rb')}).json()

    params = {'server': r['server'],
              'photo': r['photo'],
              'hash': r['hash'],
              'group_id': group_id}
    return vk.photos.saveMessagesPhoto(**params)[0]['id'], qr_path


def message_new(**kwargs):
    photo_id, qr_path = createqr_to_vk(kwargs.get('text'))

    if kwargs.get('from_chat'):
        vk.messages.send(
            chat_id=kwargs.get('from_chat'),
            random_id=0,
            message='Вот ваш купон\nprocess name: {}'.format(current_process().name),
            attachment="photo-{}_{}".format(group_id, photo_id)
        )
    elif kwargs.get('from_user'):
        vk.messages.send(
            user_id=kwargs.get('from_user'),
            random_id=0,
            message='Вот ваш купон\nprocess name: {}'.format(current_process().name),
            attachment="photo-{}_{}".format(group_id, photo_id)
        )
    os.remove(qr_path)


def err_callback(e):
    print(e)


def main():
    with Pool(os.cpu_count() * 2) as p:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
                print('пришло новое сообщение')

                if event is not None:
                    kwds = {'text': event.obj.text}
                    if event.from_user:
                        kwds['from_user'] = event.obj.from_id
                    else:
                        kwds['from_chat'] = event.chat_id
                else:
                    kwds = {}

                p.apply_async(func=message_new,
                              kwds=kwds)

                # self.message_new(event)
            elif event.type == VkBotEventType.MESSAGE_REPLY:
                print('ответ для {}'.format(event.obj.peer_id))
                print('Текст:', event.obj.text)
            elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
                print('Печатает {} для {}'.format(event.obj.from_id, event.obj.to_id))
            elif event.type == VkBotEventType.GROUP_JOIN:
                print('{} вступил в группу!'.format(event.obj.user_id))
            elif event.type == VkBotEventType.GROUP_LEAVE:
                print('{} покинул группу!'.format(event.obj.user_id))
            else:
                print(event.type)


if __name__ == '__main__':
    main()
