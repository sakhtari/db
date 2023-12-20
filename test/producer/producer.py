import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_keys = ['displays.exterior', 'displays.interior.reservation']
message = {'key': 'value'}  # Assuming you are sending a dictionary

for routing_key in routing_keys:
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=json.dumps(message))
    print(f" [x] Sent '{message}' with routing key '{routing_key}'")

connection.close()
