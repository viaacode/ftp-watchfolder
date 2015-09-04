import pika
import logging
from pika.credentials import PlainCredentials

__author__ = 'viaa'


def send_message(host, port, username, password, exchange, topic_type, queue, routing_key, message):
        logging.debug("Connecting to Rabbit MQ")
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=PlainCredentials(username, password)
        ))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, type=topic_type)
        channel.queue_declare(queue=queue)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        connection.close()
        logging.debug("Message published to: " + exchange + "/" + routing_key)

