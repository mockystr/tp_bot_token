import os
import time
import hashlib
import pika
import pickle
from multiprocessing import Pool, current_process
from main import createqr_to_vk


def callback(ch, method, properties, body):
    start = time.time()
    body = pickle.loads(body)
    print("[x] {} received {}".format(current_process(), body))
    body['photo_id'] = createqr_to_vk(body.get('text'))
    ch.basic_publish(exchange='',
                     routing_key='message_queue',
                     body=pickle.dumps(body)
                     )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(time.time() - start)


def consume():
    print('[*]{} Waiting for qr tasks. To exit press CTRL+C'.format(current_process().name))
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tpbot')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=callback, queue='tpbot')
    channel.start_consuming()


if __name__ == '__main__':
    workers = os.cpu_count() * 2

    with Pool(processes=workers) as pool:
        for i in range(workers):
            pool.apply_async(consume)

        try:
            while True:
                continue
        except KeyboardInterrupt:
            print('[*] Exiting...')
            pool.terminate()
            pool.join()