import pika
from pika import channel
from pika.exchange_type import ExchangeType

from src.config import rabbitmq
from src.services.audio_extractor import AudioExtractor

class MessageConsumer:
    def __init__(self):
        self.__parameters = pika.URLParameters(f"amqp://{rabbitmq.get('rabbitmq_user')}:{rabbitmq.get('rabbitmq_password')}@{rabbitmq.get('rabbitmq_host')}:{rabbitmq.get('rabbitmq_port')}/%2F")


    def consume(self):
        self.__connection = pika.SelectConnection(parameters=self.__parameters, on_close_callback=self.__handle_connection_close, on_open_callback=self.__handle_connection_open, on_open_error_callback=self.__handle_connection_open_error)
        self.__connection.ioloop.start()

    def __handle_audio_extraction(self, ch, method, properties, body):
        AudioExtractor().extract(body)
        return

    def __handle_connection_close(self, connection, reason):
        print("connection closed...", reason)


    def __handle_connection_open(self, connection: pika.SelectConnection):
        connection.channel(on_open_callback=self.__handle_channel_open)

    def __handle_channel_open(self, channel: channel.Channel):
        self.__channel = channel
        self.__channel.exchange_declare(exchange="exc.audio.extractor", exchange_type=ExchangeType.direct)
        self.__channel.queue_declare(queue='queue.audio.extractor')
        self.__channel.queue_bind(queue='queue.audio.extractor', exchange='exc.audio.extractor', routing_key='key.extractor')
        self.__channel.add_on_cancel_callback(self.__on_consumer_canceled)
        self.__channel.basic_consume(queue='queue.audio.extractor', auto_ack=True, on_message_callback=self.__handle_audio_extraction)

    def __handle_connection_open_error(self):
        print("connection open error...")

    def __on_consumer_canceled(self):
        pass