import pika
import json

RABBITMQ_HOST = 'localhost' # Use 'localhost' if running outside Docker, or 'rabbitmq' if inside

def consume_events():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the exchange to ensure it exists
        channel.exchange_declare(exchange='order_events', exchange_type='topic')

        # Declare an exclusive queue for this consumer
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange and routing key
        channel.queue_bind(exchange='order_events', queue=queue_name, routing_key='order.completed')

        print(' [*] Waiting for order.completed events. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(f" [x] Received event: {body.decode()}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    consume_events()
