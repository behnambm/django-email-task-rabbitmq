import pika
from pika.spec import PERSISTENT_DELIVERY_MODE

params = pika.ConnectionParameters(host="localhost")


def publish(email):
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()
    channel.queue_declare(queue="email_task_queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="email_task_queue",
        body=email,
        properties=pika.BasicProperties(
            delivery_mode=PERSISTENT_DELIVERY_MODE
        ),
    )
    channel.close()
