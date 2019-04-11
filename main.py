import os
import pickle
import pika
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from qr import createqr
from settings import token, group_id

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tpbot')

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id, wait=25)
upload = vk_api.VkUpload(vk_session)


def createqr_to_vk(text):
    qr_path, qr_img = createqr(text)
    r = upload.photo_messages(qr_path)
    os.remove(qr_path)
    return r[0]['id']


def new_message(**kwargs):
    if kwargs.get('from_chat'):
        vk.messages.send(
            chat_id=kwargs.get('from_chat'),
            random_id=0,
            message='Вот ваш купон',
            attachment="photo-{}_{}".format(group_id, kwargs.get('photo_id'))
        )
    elif kwargs.get('from_user'):
        vk.messages.send(
            user_id=kwargs.get('from_user'),
            random_id=0,
            message='Вот ваш купон',
            attachment="photo-{}_{}".format(group_id, kwargs.get('photo_id'))
        )


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
            print(event.obj.text)
            kwds = {'text': event.obj.text}
            if event.from_user:
                kwds['from_user'] = event.obj.from_id
            else:
                kwds['from_chat'] = event.chat_id
            kwds = pickle.dumps(kwds)

            channel.basic_publish(exchange='',
                                  routing_key='tpbot',
                                  body=kwds
                                  )


if __name__ == '__main__':
    main()