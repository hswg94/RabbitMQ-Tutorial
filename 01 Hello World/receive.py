#!/usr/bin/env python
import pika, sys, os

def main():
    # Establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # Create a channel
    channel = connection.channel()
    # Declare a queue named 'hello'
    channel.queue_declare(queue='hello')
    # Define a callback function to process received messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Set up subscription on the 'hello' queue
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Enter a blocking loop to wait for messages
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)