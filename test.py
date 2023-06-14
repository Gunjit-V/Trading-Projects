import pika
import time

# Message Queue Code
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='ws_data')

for i in range(0, 100):
    channel.basic_publish(
        exchange='', routing_key='ws_data', body=f"Hello World {i}")
    time.sleep(0.5)
print("Done")
