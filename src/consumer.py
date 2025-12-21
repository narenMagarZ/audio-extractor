from aio_pika.exchange import ExchangeType
import json
from aio_pika import connect, Connection, Channel
from aio_pika.queue import AbstractQueue

from src.config import rabbitmq
from src.services.audio_extractor import AudioExtractor
from src.logger import Logger

class MessageConsumer:
    __connection: Connection
    __channel: Channel
    __queue: AbstractQueue
    def __init__(self):
        pass

    async def connect(self):
        self.__connection = await connect(f"amqp://{rabbitmq['rabbitmq_user']}:{rabbitmq['rabbitmq_password']}@{rabbitmq['rabbitmq_host']}:{rabbitmq['rabbitmq_port']}/")
        self.__channel = await self.__connection.channel()

        exchange = await self.__channel.declare_exchange(name="exe.audio.extractor", type=ExchangeType.DIRECT)
        self.__queue = await self.__channel.declare_queue(name="queue.audio.extractor")
        await self.__queue.bind(exchange, routing_key="key.extractor")

    
    async def consume(self):
        async with self.__queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.__handle_message(message.body)

    async def __handle_message(self, payload: bytes):
        data = json.loads(payload)
        await AudioExtractor().extract(data)


    async def close(self):
        self.__channel.close()
        self.__connection.close()

