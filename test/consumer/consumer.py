import pika
import json

def callback_exterior(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received {message} for displays.exterior")

def callback_interior(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received {message} for displays.interior.reservation")

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

routing_patterns = ['displays.exterior', 'displays.interior.reservation']
for pattern in routing_patterns:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=pattern)

channel.basic_consume(queue=queue_name, on_message_callback=callback_exterior, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback_interior, auto_ack=True)

print(f' [*] Waiting for messages with routing patterns: {routing_patterns}')
channel.start_consuming()
