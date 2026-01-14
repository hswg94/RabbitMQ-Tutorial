#!/usr/bin/env python
import pika, sys, os, time

def main():
    # Establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    # Create a channel
    channel = connection.channel()
    qname = 'hello'
    # Declare a queue named 'hello'
    # Durable=True is so messages are not lost when RabbitMQ quits or crashes
    channel.queue_declare(queue=qname, durable=True)
    # To not give more than one message to a worker at a time
    channel.basic_qos(prefetch_count=1)
    # Define a callback function to process received messages
    # Set up subscription on the 'hello' queue
    channel.basic_consume(queue=qname, on_message_callback=callback, auto_ack=False)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    # Enter a blocking loop to wait for messages
    channel.start_consuming()

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # Acknowledge the message
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
