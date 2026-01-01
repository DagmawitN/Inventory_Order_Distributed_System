import pika
import json

RABBITMQ_HOST = 'rabbitmq'

def publish_order_completed(order_data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='order_events', exchange_type='topic')
        
        channel.basic_publish(
            exchange='order_events',
            routing_key='order.completed',
            body=json.dumps(order_data)
        )
        connection.close()
        print(" [x] Sent 'order.completed'")
    except Exception as e:
        print(f"Failed to publish event: {e}")

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f" [x] Received inventory.low_stock: {data}")
    # Handle low stock alert 

def listen_inventory_low_stock():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='inventory_events', exchange_type='topic')
        
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        
        channel.queue_bind(exchange='inventory_events', queue=queue_name, routing_key='inventory.low_stock')
        
        print(' [*] Waiting for inventory.low_stock events. To exit press CTRL+C')
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to start listener: {e}")
