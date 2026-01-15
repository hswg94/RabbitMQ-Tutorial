#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
# A direct exchange routes messages to a queue with a matching routing key
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# create a queue with a random name, exclusive true means the queue is deleted when the connection is closed
result = channel.queue_declare(queue='', exclusive=True)
# get the name of the randomly generated queue
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# bind the queue to the exchange with the specified routing keys (severities)
# running python receive_logs_direct.py info warning error will bind the queue to all 3 routing keys
for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body.decode()}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()