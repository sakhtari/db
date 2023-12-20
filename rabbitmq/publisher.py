import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = "Hello, RabbitMQ!"

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(f" [x] Sent '{message}'")

connection.close()
