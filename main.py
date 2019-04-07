from settings import token, group_id, save_path
from qr import QR
from multiprocessing import Pool, Process, current_process
import random
import sys
import requests
import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from jinja2 import Template
import time
import pickle
from functools import partial


def testing(*args, **kwargs):
    print(args, kwargs)
    return 1 ** 2


# def message_new(event, vk):
# print(event, vk)
# bot = Bot()
# print('event', event)
# photo_id, qr_path = bot.createqr_to_vk(event.obj.text)
# print('wdwdwdwd')
# if event.from_chat:
#     vk.messages.send(
#         chat_id=event.chat_id,
#         random_id=random.randint(1, pow(10, 6)),
#         message='Вот ваш купон',
#         attachment="photo-{}_{}".format(group_id, photo_id)
#     )
# elif event.from_user:
#     vk.messages.send(
#         user_id=event.obj.from_id,
#         random_id=random.randint(1, pow(10, 6)),
#         message='Вот ваш купон',
#         attachment="photo-{}_{}".format(group_id, photo_id)
#     )
# os.remove(qr_path)
# return event
# return event ** 2


class Bot:
    def __init__(self):
        self.index_html = open('static/index.html').read()
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, 180619567, wait=25)
        self.upload_url = self.vk.photos.getMessagesUploadServer(group_id=group_id)['upload_url']

    def createqr_to_vk(self, text):
        print('process name: {}'.format(current_process().name))
        qr = QR()
        qr_path, qr_img = qr.createqr(text)
        # print(qr_path, qr_img)

        r = requests.post(self.upload_url,
                          files={'photo': open(qr_path, 'rb')}).json()

        params = {'server': r['server'],
                  'photo': r['photo'],
                  'hash': r['hash'],
                  'group_id': group_id}
        # print(params)
        return self.vk.photos.saveMessagesPhoto(**params)[0]['id'], qr_path

    def message_new(self, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)
        # photo_id, qr_path = self.createqr_to_vk(event_obj.text)
        # if event.from_chat:
        #     self.vk.messages.send(
        #         chat_id=event.chat_id,
        #         random_id=random.randint(1, pow(10, 6)),
        #         message='Вот ваш купон',
        #         attachment="photo-{}_{}".format(group_id, photo_id)
        #     )
        # elif event.from_user:
        #     self.vk.messages.send(
        #         user_id=event.obj.from_id,
        #         random_id=random.randint(1, pow(10, 6)),
        #         message='Вот ваш купон',
        #         attachment="photo-{}_{}".format(group_id, photo_id)
        #     )
        # os.remove(qr_path)

    def err_callback(self, e):
        print(e)

    def main(self):
        with Pool(os.cpu_count() * 2) as p:
            for event_obj in self.longpoll.listen():
                if event_obj.type == VkBotEventType.MESSAGE_NEW and event_obj.obj.text:
                    print('пришло новое сообщение')
                    # print(event, type(event))
                    # pickle.dump(event, open('asd.pickle', 'wb'))
                    eventstr = pickle.dumps(obj=event_obj)
                    print(eventstr)
                    # if event is not None and event.obj is not None:
                    #     kwds = {'text': event.obj.text}
                    #     if event.from_user:
                    #         kwds['from_user'] = event.obj.from_id
                    #     else:
                    #         kwds['from_chat'] = event.chat_id
                    # else:
                    #     kwds = {}
                    #     print('event is none', event)
                    # print('kwds', kwds)
                    # r = p.apply_async(func=self.message_new,
                    #                   args=(self, kwds.keys()), ).\
                    #     get()
                    # print('performed')
                    # print('r_dict_', r.__dict__)
                    # r.wait()
                    # print(r.successful())

                    # self.message_new(event)
                    """event ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', 'chat_id', 'from_chat', 'from_group', 'from_user', 'group_id', 'obj', 'object', 'raw', 't', 'type']
                       event.obj {'date': 1554550298, 'from_id': 170285902, 'id': 330, 'out': 0, 'peer_id': 170285902, 'text': 'd', 'conversation_message_id': 323, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}
                    """
                    # print('success', r.successful())
                    # print('ready', r.ready())
                    # if r.successful():
                    #     print(r.get())
                # elif event.type == VkBotEventType.MESSAGE_REPLY:
                #     print('ответ для {}'.format(event.obj.peer_id))
                #     print('Текст:', event.obj.text)
                # elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
                #     print('Печатает {} для {}'.format(event.obj.from_id, event.obj.to_id))
                # elif event.type == VkBotEventType.GROUP_JOIN:
                #     print('{} вступил в группу!'.format(event.obj.user_id))
                # elif event.type == VkBotEventType.GROUP_LEAVE:
                #     print('{} покинул группу!'.format(event.obj.user_id))
                # else:
                #     print(event.type)
                # except Exception as a


if __name__ == '__main__':
    bot = Bot()
    bot.main()
