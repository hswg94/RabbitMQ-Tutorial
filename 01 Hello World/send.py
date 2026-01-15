#!/usr/bin/env python
import pika

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# Create a channel
channel = connection.channel()

qname = 'hello'
# Declare a queue named 'hello'
channel.queue_declare(queue=qname)


# Publish a message to the 'hello' queue
channel.basic_publish(exchange='',
                      routing_key=qname,
                      body='Hello World!')

print(f"Sent 'Hello World!' to the '{qname}' queue")

# Close the connection
connection.close()