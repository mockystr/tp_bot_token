from settings import token, group_id
from qr import QR
from multiprocessing import Pool, current_process
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
        self.longpoll = VkBotLongPoll(self.vk_session, group_id, wait=25)
        self.upload = vk_api.VkUpload(self.vk_session)

    def testing(self, *args, **kwargs):
        print(args, kwargs)
        return 1 ** 2

    def createqr_to_vk(self, text):
        print('process name: {}'.format(current_process().name))
        qr = QR()
        qr_path, qr_img = qr.createqr(text)
        r = self.upload.photo_messages(qr_path)
        return r[0]['id'], qr_path

    def message_new(self, **kwargs):
        photo_id, qr_path = self.createqr_to_vk(kwargs.get('text'))

        print('before sendingd')
        if kwargs.get('from_chat'):
            self.vk.messages.send(
                chat_id=kwargs.get('from_chat'),
                random_id=0,
                message='Вот ваш купон\nprocess name: {}'.format(current_process().name),
                attachment="photo-{}_{}".format(group_id, photo_id)
            )
        elif kwargs.get('from_user'):
            self.vk.messages.send(
                user_id=kwargs.get('from_user'),
                random_id=0,
                message='Вот ваш купон\nprocess name: {}'.format(current_process().name),
                attachment="photo-{}_{}".format(group_id, photo_id)
            )
        os.remove(qr_path)

    def err_callback(self, e):
        print(e)

    def main(self):
        with Pool(os.cpu_count()) as p:
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
                    print('пришло новое сообщение')
                    start = time.time()

                    if event is not None:
                        kwds = {'text': event.obj.text}
                        if event.from_user:
                            kwds['from_user'] = event.obj.from_id
                        else:
                            kwds['from_chat'] = event.chat_id
                    else:
                        kwds = {}

                    r = p.apply_async(func=Bot.testing, args=(self,))
                    r.wait()
                    print(r.successful())
                    # False
                    print(r.get())
                    # Traceback (most recent call last):
                    #   File "/Users/emirnavruzov/Documents/technopark/tp_token_bot/main.py", line 91, in <module>
                    #     Bot().main()
                    #   File "/Users/emirnavruzov/Documents/technopark/tp_token_bot/main.py", line 72, in main
                    #     print(r.get())
                    #   File "/anaconda3/lib/python3.7/multiprocessing/pool.py", line 657, in get
                    #     raise self._value
                    #   File "/anaconda3/lib/python3.7/multiprocessing/pool.py", line 431, in _handle_tasks
                    #     put(task)
                    #   File "/anaconda3/lib/python3.7/multiprocessing/connection.py", line 206, in send
                    #     self._send_bytes(_ForkingPickler.dumps(obj))
                    #   File "/anaconda3/lib/python3.7/multiprocessing/reduction.py", line 51, in dumps
                    #     cls(buf, protocol).dump(obj)
                    # TypeError: 'NoneType' object is not callable


                    # message_new(**kwds)
                    print('finish {:.6f}s'.format(time.time() - start))
                    print()
                    print()
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
    Bot().main()
