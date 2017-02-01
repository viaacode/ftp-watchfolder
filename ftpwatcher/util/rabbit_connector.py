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
        self.connection_attempts = 50
        self.retry_delay = 10000
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, type=topic_type)
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

    def send_message(self, message):
        logging.info("Publishing message")
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message,
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        logging.info("Message published to: " + self.exchange + "/" + self.routing_key)

    def close_connection(self):
        logging.info("Closing RabbitMQ connection")
        self.channel.close()
        self.connection.close()
