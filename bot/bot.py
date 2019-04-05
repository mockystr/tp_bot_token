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

    def message_new(self, event):
        photo_id, qr_path = self.createqr_to_vk(event.obj.text)

        if event.from_chat:
            self.vk.messages.send(
                chat_id=event.chat_id,
                random_id=random.randint(1, pow(10, 6)),
                message='Вот ваш купон',
                attachment="photo-{}_{}".format(group_id, photo_id)
            )
        elif event.from_user:
            self.vk.messages.send(
                user_id=event.obj.from_id,
                random_id=random.randint(1, pow(10, 6)),
                message='Вот ваш купон',
                attachment="photo-{}_{}".format(group_id, photo_id)
            )
        os.remove(qr_path)

    def main(self):
        with Pool() as p:
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
                    p.map(self.message_new, [event])

                    # p.close()
                    # p.join()
                    # time.sleep(1)
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
                # except Exception as a


if __name__ == '__main__':
    bot = Bot()
    bot.main()
