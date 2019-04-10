from multiprocessing import Pool, current_process
import time
import os
import pika
import pickle
from main import message_new


def callback(ch, method, properties, body):
    start = time.time()
    body = pickle.loads(body)
    print("[x] {} received {}".format(current_process(), body))
    message_new(**body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(time.time() - start)


def consume():
    print('[*]{} Waiting for messages. To exit press CTRL+C'.format(current_process().name))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tpbot', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=callback, queue='tpbot')
    channel.start_consuming()


if __name__ == '__main__':
    workers = os.cpu_count() * 2 - 1

    with Pool(processes=workers) as pool:
        for i in range(0, workers):
            pool.apply_async(consume)

        try:
            while True:
                continue
        except KeyboardInterrupt:
            print('[*] Exiting...')
            pool.terminate()
            pool.join()
