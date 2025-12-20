import pika
from pika.exchange_type import ExchangeType
import json
from pika import channel

from src.config import rabbitmq
from src.logger import Logger
  
class MessageProducer:
  def __init__(self):
    self.__parameters = pika.URLParameters(f"amqp://{rabbitmq.get('rabbitmq_user')}:{rabbitmq.get('rabbitmq_password')}@{rabbitmq.get('rabbitmq_host')}:{rabbitmq.get('rabbitmq_port')}/%2F")

  def connect(self):
    self.__connection = pika.SelectConnection(parameters=self.__parameters, on_close_callback=self.__handle_connection_close, on_open_callback=self.__handle_connection_open, on_open_error_callback=self.__handle_connection_open_error)
    self.__connection.ioloop.start()

  def __handle_connection_close(self, connection, reason):
    Logger().error(f"Connection to producer closed: {reason}")

  def __handle_connection_open(self, connection: pika.SelectConnection):
    Logger().info("Connection to producer established successfully...")
    connection.channel(on_open_callback=self.__handle_channel_open)

  def __handle_channel_open(self, channel: channel.Channel):
    self.__channel = channel
    self.__channel.exchange_declare(exchange="exc.audio.extractor", exchange_type=ExchangeType.direct)
    self.__channel.queue_declare(queue='queue.audio.extractor')
    self.__channel.queue_bind(queue='queue.audio.extractor', exchange='exc.audio.extractor', routing_key='key.extractor')

  def __handle_connection_open_error(self):
    Logger.error(f"Failed to create connection to producer")

  def produce(self, msg: any):
    self.__channel.basic_publish(
        exchange="exc.audio.extractor", 
        routing_key='key.extractor', 
        body=json.dumps(msg), 
        properties=pika.BasicProperties(content_type='application/json')
      )

message_producer = MessageProducer()