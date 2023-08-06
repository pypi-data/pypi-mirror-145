import os
import traceback

from sys import exit
from ast import literal_eval
from typing import Any, Dict
from cosecurity_amqp_lib.logger import logger
from pika import BlockingConnection, ConnectionParameters


class Consumer:
    """
    queue consumer with a general handler to handle posted messages
    """
    def __init__(self, name:str) -> None:
        self._host = os.getenv('AMQP_HOST', None)
        if self._host is None:
            raise Exception('The environment variable AMQP_HOST is required for operation')

        self._heartbeat = os.getenv('AMQP_HEARTBEAT', None)
        if self._heartbeat is None:
            raise Exception('The environment variable AMQP_HEARTBEAT is required for operation')
        self._heartbeat = eval(self._heartbeat)

        self._queue_name = os.getenv(f'{name.upper()}_QUEUE', None)
        if self._queue_name is None:
            raise Exception('Queue not found in configuration file, please review!')

        self._name = name
        self._handlers = {}

    def register(self, handler:Any) -> bool:
        if not hasattr(handler, '__name__') or handler.__name__ in self._handlers:
            return False

        self._handlers[handler.__name__] = handler
        return True

    def start(self) -> None:
        try:
            self._connection = BlockingConnection(
                ConnectionParameters(
                    host=self._host, 
                    heartbeat=self._heartbeat
                )
            )
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue_name)

            self._channel.basic_consume(
                queue=self._queue_name,
                on_message_callback=self._callback_method,
                auto_ack=True
            )

            logger.info(f'{self._name} initialized')
            self._channel.start_consuming()
        except:
            self._channel.stop_consuming()
            self._channel.close()
            self._connection.close()
            logger.info(f'{self._name} finished')
            exit()
            
    def _callback_method(self, ch:str, method:str, properties:Dict[str, Any], body:str) -> None:
        try:
            message = self._binary_to_dict(body)
            if not (('primitive' in message and 'content' in message) and (isinstance(message['primitive'], str) and isinstance(message['content'], dict))):
                raise Exception("""
                    It is necessary to include in the message the key 'primitive' that contains the name of the action and 'content' 
                    that has the parameters for the action
                """)

            self._handle_message(message)
        except:
            logger.error(traceback.print_exc())

    def _binary_to_dict(self, binary_json:str) -> Dict[str, Any]:
        return literal_eval(binary_json.decode('utf-8'))

    def _handle_message(self, message:Dict[str, Any]) -> None:
        if self._handlers and message['primitive'] in self._handlers:
            self._handlers[message['primitive']](message['content'])
        else:
            logger.info(f'No implementation for {message} found!')
