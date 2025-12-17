from threading import Lock
import pika
from pika.exchange_type import ExchangeType
import json

from src.enum.message_producer_enum import ExchangeEnum
from src.config import rabbitmq

class RabbitmqSingletonMeta(type):
  __instance = None
  __lock: Lock = Lock()
    
  def __call__(self, *args, **kargs):
    with self.__lock:
      print(self.__instance, 'instance before instantiate')
      if self.__instance is None:
        self.__instance = super().__call__(*args, **kargs)
      print(self.__instance, 'instance', 'after instantiate')
    return self.__instance

class RabbitMq(metaclass=RabbitmqSingletonMeta):
  __parameters: pika.URLParameters
  __connection: pika.SelectConnection

  def __init__(self):
    self.__parameters = pika.URLParameters(f"amqp://{rabbitmq.get('rabbitmq_user')}:{rabbitmq.get('rabbitmq_password')}@{rabbitmq.get('rabbitmq_host')}:{rabbitmq.get('rabbitmq_port')}/%2F")
    self.connect()


  def connect(self):
    try:
      self.__connection = pika.SelectConnection(parameters=self.__parameters, on_close_callback=self.__handle_connection_close, on_open_callback=self.__handle_connection_open, on_open_error_callback=self.__handle_connection_open_error)
    except Exception as e:
      raise

  def __handle_connection_close(self, connection, reason):
    print("connection closed...")

  def __handle_connection_open(self, connection: pika.SelectConnection):
    print("connection opened...")
    connection.channel(on_open_callback=self.__handle_channel_open)

  def __handle_channel_open(self, channel):
    print("channel opened...")
    self.__channel = channel
    self.__channel.exchange_declare(exchange="exc.audio.extractor", exchange_type=ExchangeType.direct)
    self.__channel.queue_declare(queue='queue.audio.extractor')
    self.__channel.queue_bind(queue='queue.audio.extractor', exchange='exc.audio.extractor', routing_key='key.extractor')


  def __handle_connection_open_error(self):
    print("connection open error...")

  def close(self):
    try:
      self.__connection.close()
    except Exception as e:
      raise

  def get_channel(self):
    return self.__channel
  
  def get_connection(self):
    return self.__connection
  

class MessageProducer:
  def __init__(self):
    self.__channel = RabbitMq().get_channel()
    RabbitMq().get_connection().ioloop.start()

  def produce(self, msg: any):
    return self.__channel.basic_publish(
        exchange="exc.audio.extractor", 
        routing_key='key.extractor', 
        body=json.dumps(msg), 
        properties=pika.BasicProperties(content_type='application/json')
      )



class MessageConsumer:
  def __init__(self):
    pass
    # self.__channel = RabbitMq().get_channel()
    # RabbitMq().get_connection().ioloop.start()

  def consume(self):
    self.__channel.basic_consume(queue='queue.audio.extractor', on_message_callback=self.__handle_audio_extraction)
  
  def __handle_audio_extraction(self):
    print("handled successfully....")

message_producer = MessageProducer()
message_consumer = MessageConsumer()