import pika


connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare(queue="audio_extraction")
