#!/usr/bin/env python
import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel() # Create a channel
        # Declare a unique, temporary callback queue that closes when the client disconnects
        result = self.channel.queue_declare(queue='', exclusive=True)
        # Get the name of the callback queue
        self.callback_queue = result.method.queue

        # Set up subscription on the callback queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            # when the client receives a response from the server, the on_response method is called
            on_message_callback=self.on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # Publish the request message to the 'rpc_queue'
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        # Client waits until there is a response
        while self.response is None:
            self.connection.process_data_events(time_limit=60)
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(40)
print(f" [.] Got {response}")