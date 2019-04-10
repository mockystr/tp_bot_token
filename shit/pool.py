from settings import token, group_id
from qr import QR
from multiprocessing import current_process
import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from jinja2 import Template
import time
from functools import partial
from multiprocessing import Pool


class Bot:
    def __init__(self):
        self.test = 100
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id, wait=25)
        self.upload = vk_api.VkUpload(self.vk_session)
        self.Pool = Pool(os.cpu_count())

    def testing(self):
        return 100 ** 2

    def main(self):
        with self.Pool as p:
            for event in range(5):
                print('пришло новое сообщение')
                r = p.apply_async(self.testing, args=())
                print(r.get())
                # message_new(**kwds)
                print()


if __name__ == '__main__':
    Bot().main()
