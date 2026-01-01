import json
import pika
import os


def publish_user_registered(user):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "rabbitmq"))
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange="events",
        exchange_type="fanout",
        durable=True,
    )

    channel.basic_publish(
        exchange="events",
        routing_key="",
        body=json.dumps({
            "event": "user.registered",
            "user_id": user.id,
            "email": user.email,
        }),
    )

    connection.close()

def publish_order_completed(user_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "rabbitmq"))
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange="events",
        exchange_type="fanout",
        durable=True,
    )

    channel.basic_publish(
        exchange="events",
        routing_key="",
        body=json.dumps({
            "event": "order.completed",
            "user_id": user_id,
        }),
    )

    connection.close()
