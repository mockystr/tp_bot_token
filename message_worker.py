import pika
from main import new_message
import time
import pickle
from multiprocessing import current_process

queue_name = 'message_queue'
RPS_DELAY = 0.34


def callback(ch, method, properties, body):
    start = time.time()

    body = pickle.loads(body)
    print("[x] {} received {}".format(current_process(), body))
    new_message(**body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    last = time.time() - start
    print(last)
    delay = RPS_DELAY - (time.time() - last)
    if delay > 0:
        time.sleep(delay)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=callback, queue=queue_name)
    channel.start_consuming()
