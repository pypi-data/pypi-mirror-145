# AMQP Internal Library
Internal library for exchanging messages between services instantiated in the AWS environment. 
The base used for the elaboration of the package was the PIKA library developed by the RabbitMQ team.

The library can be found on Pypi at the link below: https://pypi.org/project/cosecurity-amqp-lib/

## Installation
To use the library it is necessary to have [Python3](https://www.python.org/downloads/) and [Docker](https://www.docker.com/products/docker-desktop/)
installed on the machine and run the following command:
```bash
sh run-rabbitmq-docker.sh
python3 -m pip install cosecurity-amqp-lib
```

## Deploy to Pypi
To send new implementations to Pypi, just change the code and increment the version in the [setup.py file](https://github.com/CoSecurity/amqp-internal-library/blob/main/setup.py#L8).
After changing, we must run the following command:
```bash
sh run-publish-pypi.sh
```

## Environment Variables File
- `AMQP_HOST` host for connecting to RabbitMQ
- `AMQP_HEARTBEAT` heartbeat timeout value defines after what period of time the peer TCP connection should be considered unreachable (down) by RabbitMQ and client libraries
- `[SERVICE_NAME]` service name and respective service queue name, can be more than one 

## Consumers 
Consumers are instances that monitor a specific queue, and if there is a change in the queue, they perform a certain action.<br>
In this library a consumer can have more than one action/method, called `primitive`. In addition, each action will still have its default input set.
Each method that must be an action must be registered so that it can be triggered if there is a change in the directed queue.<br>
Below is an example of how to create a consumer class:
```python
from typing import Any, Dict
from cosecurity_amqp_lib.consumer import Consumer

class ConsumerExample(Consumer):
    def __init__(self) -> None:
        super().__init__(
            name='example'
        )
        self.register(self.primitive_one)
        self.register(self.primitive_two)
        self.start()
    
    def primitive_one(self, content:Dict[str, Any]) -> None:
        print(content['hello'])
    
    def primitive_two(self, content:Dict[str, Any]) -> None:
        print(content['message'])
```

## Producers
Producers are responsible for producing and/or posting new messages in consumer queues. <br>
In the internal library the producers are called `stub`, I try their methods defined and typed based on what has already been defined as `primitive` in their consumer.<br>
Below is an example of how to create a `stub` inside the library in the [stub.py file](https://github.com/CoSecurity/amqp-internal-library/blob/main/cosecurity_amqp_lib/stub.py):
```python
class ExampleStub(Stub):
    def __init__(self):
        super().__init__(
            destination='example'
        )

    def primitive_one(self) -> None:
        self._send(
            primitive='primitive_one',  
            content={
                'hello': 'word'
            }
        )

    def primitive_two(self, message:str) -> None:
        self._send(
            primitive='primitive_two',  
            content={
                'message': message
            }
        )
```
Now, an example of how to use an already created `stub` and publish it in the library in Pypi:
```python
from cosecurity_amqp_lib.stub import ExampleStub

example_stub = ExampleStub()
example_stub.primitive_one()
example_stub.primitive_two(message='Hello world!')
```
## Example
In the [example/simple](https://github.com/CoSecurity/amqp-internal-library/tree/main/example/simple) 
folder we have a real case example of a `stub` sending an string to a consumer.
