# import multiprocessing
# import time
#
# import pika
#
#
# def callback(ch, method, properties, body):
#     print(" [x] %r received %r" % (multiprocessing.current_process(), body,))
#     time.sleep(0.5)
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
# def consume():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(
#         'localhost'))
#     channel = connection.channel()
#     print('im here')
#     channel.queue_declare(queue='hello', durable=True)
#     print('imhere2')
#     channel.basic_consume(queue='hello', on_message_callback=callback)
#     print('asdasdas')
#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     try:
#         channel.start_consuming()
#     except KeyboardInterrupt:
#         pass
#
#
# workers = 5
# pool = multiprocessing.Pool(processes=workers)
# for i in range(0, workers):
#     pool.apply_async(consume)
#
# # Stay alive
# try:
#     while True:
#         continue
# except KeyboardInterrupt:
#     print(' [*] Exiting...')
#     pool.terminate()
#     pool.join()

from multiprocessing import Pool, current_process
import time
import os
import pika


def callback(ch, method, properties, body):
    print("[x] {} received {}".format(current_process(), body))
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    print('[*]{} Waiting for messages. To exit press CTRL+C'.format(current_process().name))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=callback, queue='hello')
    channel.start_consuming()


workers = os.cpu_count()
pool = Pool(processes=workers)
with pool:
    for i in range(0, workers):
        pool.apply_async(consume)

    # Stay alive
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print('[*] Exiting...')
        pool.terminate()
        pool.join()
