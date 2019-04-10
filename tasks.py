import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
# channel.basic_qos(prefetch_count=1)

message = ' '.join(sys.argv[1:]) or "Hello World!"

for i in range(500):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print(" [x] Sent '{}'!".format(message))

connection.close()
