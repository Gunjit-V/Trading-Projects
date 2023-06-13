import pika


def on_message_recieved(channel, method, properties, body):
    print(body)


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='ws_data')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='ws_data', on_message_callback=on_message_recieved)

print("Started Consuming")

channel.start_consuming()
