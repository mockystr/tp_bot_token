import pika
import time
import random
import pickle

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

print('[*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    body = pickle.loads(body)
    print("[x] Received {}".format(body, ))
    time.sleep(random.randint(1, 2))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='hello', on_message_callback=callback)
channel.start_consuming()

channel.queue_declare(queue='hello')
