import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import token


def main():
    vk_session = vk_api.VkApi(token=token, scope='+4096')
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, 180619567, wait=25)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.obj.text:
            if event.from_chat:
                # mtext = event.obj.text
                # print(mtext)
                vk.messages.send(
                    chat_id=event.chat_id,
                    random_id=0,
                    message="из чата"
                )
            elif event.from_user:
                # mtext = event.obj.text
                # print(mtext)
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=0,
                    message='из лички'
                )
            print('Новое сообщение:')
            print('Для меня от: ', end='')
            print(event.obj.from_id)
            print('Текст:', event.obj.text)
            print()
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')
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


if __name__ == '__main__':
    main()
