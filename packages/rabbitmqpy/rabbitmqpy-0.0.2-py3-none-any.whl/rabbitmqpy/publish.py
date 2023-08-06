#coding:utf-8

import json
import pika
import time
from pika.exchange_type import ExchangeType

RETRY_COUNT = 5

def retry(func):

    def __wrapper__(*args, **kwarges):
        count = RETRY_COUNT
        while count>0:
            res = func(*args, **kwarges)
            if res:
                break

            count -=1
            print('reconnect channel')
            time.sleep(3)
        return res
    return __wrapper__


class Puber(object):

    def __init__(self, amqp_url, exchange, exchange_type, queue=None, routing_key=None, **kwargs):
        self._connection = None
        self._channel = None
        self._url = amqp_url
        self._exchange = exchange
        self._exchange_type = exchange_type
        self._routing_key = routing_key
        self._passive = kwargs.get("passive", False)
        self._durable = kwargs.get("durable", False)
        self._auto_delete = kwargs.get("auto_delete", True)

        self.connect()

    def connect(self):
        print('Connecting to %s', self._url)
        self._connection = pika.BlockingConnection(
            pika.URLParameters(self._url))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type=self._exchange_type,
            passive=self._passive,
            durable=self._durable,
            auto_delete=self._auto_delete
        )

    @retry
    def send(self, data):
        try:
            content_type = None
            if not isinstance(data, str):
                data = json.dumps(data)
                content_type = 'application/json'

            self._channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._routing_key,
                body=data,
                properties=pika.BasicProperties(content_type=content_type))
            print('send {}'.format(str(data)[:502]))
            return True
        except Exception as e:
            self.recreate_channel()
            print(e)

    def recreate_channel(self):
        self.connect()


    def __del__(self):
        self._connection.close()


if __name__=='__main__':
    # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    puber = Puber(
        'amqp://10.12.3.162:31911',
        'imlf-1',
        ExchangeType.direct,
        'predict',
        'predict'
    )

