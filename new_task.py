#!/usr/bin/env python
from email.mime import message
import pika
import sys

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
# Create a channel
channel = connection.channel()

qname = 'hello'
message = ' '.join(sys.argv[1:]) or "Hello World!"
# Declare a queue named 'hello', create it if needed
channel.queue_declare(queue=qname, durable=True)

# Publish a message to the 'hello' queue
# delivery_mode=2 save messages to disk within a short time window to make them persistent
channel.basic_publish(exchange='',
                      routing_key=qname,
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=pika.DeliveryMode.Persistent
                      ))

print(f"Sent '{message}' to the '{qname}' queue")

# Close the connection
connection.close()