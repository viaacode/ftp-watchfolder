import logging
import json
from json import loads, dumps
import pika
from ftpwatcher.util import rabbit_connector as rabbit
from pika.credentials import PlainCredentials

import pdb


class MD5Generator:
    def __init__(self, file_index):
        self.file_index = file_index
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.file_index.config['RABBIT_MQ_HOST'],
            port=int(self.file_index.config['RABBIT_MQ_PORT']),
            credentials=PlainCredentials(self.file_index.config['RABBIT_MQ_USER'], self.file_index.config['RABBIT_MQ_PASSWORD'])
        ))

        channel = connection.channel()
        channel.queue_declare(queue=self.file_index.config['RABBIT_MQ_MD5_RESPONSE_QUEUE'], durable=True)
        channel.basic_consume(self.callback, self.file_index.config['RABBIT_MQ_MD5_RESPONSE_QUEUE'])
        channel.start_consuming()

    def generate_md5(self, file_path, file_name):
        pdb.set_trace()
        logging.info("Sending md5 message...")
        connection = rabbit.Connector(
            host=self.file_index.config['RABBIT_MQ_HOST'],
            port=int(self.file_index.config['RABBIT_MQ_PORT']),
            username=self.file_index.config['RABBIT_MQ_USER'],
            password=self.file_index.config['RABBIT_MQ_PASSWORD'],
            exchange=self.file_index.config['RABBIT_MQ_MD5_REQUEST_EXCHANGE'],
            topic_type=self.file_index.config['RABBIT_MQ_TOPIC_TYPE'],
            queue=self.file_index.config['RABBIT_MQ_MD5_REQUEST_QUEUE'],
            routing_key=self.file_index.config['FLOW_ID']
        )
        connection.send_message(
            message=json.dumps({
                "correlation_id": "1",
                "server": "",
                "path": file_path,
                "sourcefile": file_name,
                "expected_md5": ""
            })
        )
        pass

    def callback(self, ch, method, properties, body):
        pdb.set_trace()
        try:
            status = 'OK'
            details = 'file successfully converted'
            convert_params = loads(body.decode("utf-8"))

        except Exception as e:
            logging.error(str(e))