import os

import django
import pika
from pika.spec import PERSISTENT_DELIVERY_MODE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.contrib.auth.models import User
from django.core.mail import send_mail

params = pika.ConnectionParameters(host="localhost")
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()
channel.queue_declare(queue="email_task_queue", durable=True)
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    # send email
    email = body.decode()
    try:
        send_mail(
            "welcome to my site",
            f"Hi {email!r}, Welcome to my site. This is an email that has been sent from a worker instance using RabbitMQ.",
            from_email="coolproject@mail.app",
            recipient_list=[email],
            fail_silently=False,
        )
        print("An email has been sent to %r" % email)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("error: ", e)


channel.basic_consume(queue="email_task_queue", on_message_callback=callback)


if __name__ == "__main__":
    try:
        print("Started listening to RabbitMQ. Press CTRL+C to stop...")
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        channel.close()
        connection.close()
