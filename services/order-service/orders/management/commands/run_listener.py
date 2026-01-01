from django.core.management.base import BaseCommand
from orders.rabbitmq import listen_inventory_low_stock

class Command(BaseCommand):
    help = 'Starts the RabbitMQ listener for guest.low_stock events'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting RabbitMQ listener...'))
        listen_inventory_low_stock()
