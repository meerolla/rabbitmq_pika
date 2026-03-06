
import pika

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "benchmark_queue"

def create_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

def setup_queue():
    connection = create_connection()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=False)
    connection.close()
