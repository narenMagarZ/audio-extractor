import pika
from src.enum.message_producer_enum import ExchangeEnum

class RabbitMq:
  __parameters: pika.ConnectionParameters = ""
  def __init__(self):
   self.__parameters = ""


  def connect(self):
    try:
      connection = pika.BlockingConnection(parameters=self.__parameters)
      self.__channel = connection.channel()
      
    except Exception as e:
      raise e

  def close(self):
    try:
      pass
    except Exception as e:
      raise e

class MessageProducer:
  pass

connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare(queue="audio_extraction")
channel.basic_publish(exchange=ExchangeEnum.Audio_Extraction.value, routing_key='', body='')

