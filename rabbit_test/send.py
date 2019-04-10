import pika
import sys
import pickle

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

for i in range(1):
    print(sys.argv)
    body = pickle.dumps({'asd': 12, 'vv': 2})
    print()
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=body,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print("[x] Sent '{}'".format(body))
connection.close()
