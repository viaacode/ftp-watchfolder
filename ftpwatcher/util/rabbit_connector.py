import pika
import logging
from pika.credentials import PlainCredentials


class Connector:
    def __init__(self, host, port, username, password, exchange, topic_type, queue, routing_key):
        logging.info("Connecting to Rabbit MQ")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=PlainCredentials(username, password)
        ))
        self.exchange = exchange
        self.routing_key = routing_key
        logging.info("Initiating Channel")
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, type=topic_type)
        self.channel.queue_declare(queue=queue)
        self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

    def send_message(self, message):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
        logging.info("Message published to: " + self.exchange + "/" + self.routing_key)

    def close_connection(self):
        logging.info("Closing RabbitMQ connection")
        self.channel.close()
        self.connection.close()
