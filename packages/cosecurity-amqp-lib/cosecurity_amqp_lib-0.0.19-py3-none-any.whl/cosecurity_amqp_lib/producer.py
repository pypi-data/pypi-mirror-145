import os
import json
import numpy as np

from typing import Any, Dict
from json import JSONEncoder
from cosecurity_amqp_lib.logger import logger
from pika import BlockingConnection, ConnectionParameters


class ProducerEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class ProducerChannel:
    def __init__(self, host:str, heartbeat:bool):
        self._connection = BlockingConnection(
            ConnectionParameters(
                host=host, 
                heartbeat=heartbeat
            )
        )
        self._channel = self._connection.channel()

    def __enter__(self):
        return self._channel

    def __exit__(self, type:Any, value:Any, traceback:Any):
        self._channel.close()
        self._connection.close()


class Producer:
    def __init__(self) -> None:
        self._host = os.getenv('AMQP_HOST', None)
        if self._host is None:
            raise Exception('The environment variable AMQP_HOST is required for operation')

        self._heartbeat = os.getenv('AMQP_HEARTBEAT', None)
        if self._heartbeat is None:
            raise Exception('The environment variable AMQP_HEARTBEAT is required for operation')
        self._heartbeat = eval(self._heartbeat)

    def send_message(self, destination:str, primitive:str, content:Dict[str, Any]) -> None:
        destination_queue = os.getenv(f'{destination.upper()}_QUEUE', None)
        if destination_queue is None:
            raise Exception('Recipient queue not found in configuration file, please review!')

        with ProducerChannel(self._host, self._heartbeat) as channel:
            channel.basic_publish(
                exchange='', 
                routing_key=destination_queue, 
                body=json.dumps(
                    obj={ 
                        'primitive': primitive, 
                        'content': content 
                    }, 
                    cls=ProducerEncoder
                )
            )
        
        logger.info(f'Sent to {destination}')
