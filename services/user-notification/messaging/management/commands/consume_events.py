from django.core.management.base import BaseCommand
from messaging.consumer import start_consumer

class Command(BaseCommand):
    help = "Consume RabbitMQ events"

    def handle(self, *args, **kwargs):
        start_consumer()
