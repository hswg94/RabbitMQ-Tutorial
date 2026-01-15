python -m pip install pika --upgrade


You may wish to see what queues RabbitMQ has and how many messages are in them. You can do it (as a privileged user) using the rabbitmqctl tool:

sudo rabbitmqctl list_queues

On Windows, omit the sudo:
rabbitmqctl.bat list_queues