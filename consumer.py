import pika
import json


def on_message_recieved(channel, method, properties, body):
    print(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='ws_data')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='ws_data', on_message_callback=on_message_recieved)

print("Started Consuming")

channel.start_consuming()
