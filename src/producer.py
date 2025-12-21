import json
from aio_pika.exchange import ExchangeType, Exchange
from aio_pika import connect, Channel, Connection, Message
from aio_pika.message import AbstractMessage

from src.config import rabbitmq
# from src.logger import Logger


class MessageProducer:
    __channel: Channel
    __connection: Connection
    __exchange: Exchange
    def __init__(self):
        pass
        
    async def connect(self):
        self.__connection = await connect(f"amqp://{rabbitmq['rabbitmq_user']}:{rabbitmq['rabbitmq_password']}@{rabbitmq['rabbitmq_host']}:{rabbitmq['rabbitmq_port']}/")
        self.__channel = await self.__connection.channel()

        self.__exchange = await self.__channel.declare_exchange(name="exe.audio.extractor", type=ExchangeType.DIRECT)
        queue = await self.__channel.declare_queue(name="queue.audio.extractor")
        await queue.bind(self.__exchange, routing_key="key.extractor")

    async def publish(self, msg):
        data: AbstractMessage = Message(body=json.dumps(msg).encode())
        await self.__exchange.publish(data, "key.extractor")


    async def close(self):
        await self.__channel.close()
        await self.__connection.close()
