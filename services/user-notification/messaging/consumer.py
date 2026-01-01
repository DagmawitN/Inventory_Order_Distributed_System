import os
import time
import pika
import json
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from notifications.models import Notification
from django.contrib.auth.models import User


def callback(ch, method, properties, body):
    data = json.loads(body)

    if data.get("event") == "order.completed":
        user = User.objects.get(id=data["user_id"])
        Notification.objects.create(
            user=user,
            type="order",
            content="Your order has been completed 🎉",
            status="sent",
        )
        print("✅ Notification sent")


def run():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

    while True:
        try:
            print("⏳ Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host)
            )
            channel = connection.channel()

            # ✅ MUST be fanout
            channel.exchange_declare(
                exchange="events",
                exchange_type="fanout",
                durable=True,
            )

            # ✅ Durable named queue (NO MESSAGE LOSS)
            channel.queue_declare(
                queue="notifications",
                durable=True,
            )

            channel.queue_bind(
                exchange="events",
                queue="notifications",
            )

            channel.basic_consume(
                queue="notifications",
                on_message_callback=callback,
                auto_ack=True,
            )

            print("🐇 Waiting for events...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ not ready. Retrying in 5s...")
            time.sleep(5)

        except Exception as e:
            print("🔥 Consumer error:", e)
            time.sleep(5)


if __name__ == "__main__":
    run()
