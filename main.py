from settings import token, group_id
from qr import QR
from multiprocessing import Pool, current_process
import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time
import pika
import pickle

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tpbot', durable=True)

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id, wait=25)
upload = vk_api.VkUpload(vk_session)


def createqr_to_vk(text):
    print('process name: {}'.format(current_process().name))
    qr = QR()
    qr_path, qr_img = qr.createqr(text)
    r = upload.photo_messages(qr_path)
    return r[0]['id'], qr_path


def message_new(**kwargs):
    photo_id, qr_path = createqr_to_vk(kwargs.get('text'))
    print(qr_path)

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


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
            print('пришло новое сообщение')
            kwds = {'text': event.obj.text}
            if event.from_user:
                kwds['from_user'] = event.obj.from_id
            else:
                kwds['from_chat'] = event.chat_id
            kwds = pickle.dumps(kwds)

            channel.basic_publish(exchange='',
                                  routing_key='tpbot',
                                  body=kwds,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
            # message_new(**kwds)


if __name__ == '__main__':
    main()
