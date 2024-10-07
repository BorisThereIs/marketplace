import sys
import os

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from dotenv import load_dotenv
load_dotenv()
sys.path.insert(1, os.environ.get('PROJECT_ROOT_DIR',
                                  '/home/superuser/practice/projects/marketplace'))

from .consts import QUEUE_PARAMS_MAPPING, QUEUE_NAME_MAPPING
from config import settings


def create_rabbit_channel() -> BlockingChannel:
    connection = BlockingConnection(ConnectionParameters(
        host=settings.MESSAGE_BROKER['host'],
        heartbeat=0))
    channel = connection.channel()
    return channel

def get_channel(exchange_name: str,
                exchange_type: str,
                queue: str,
                routing_key: str) -> BlockingChannel:
    channel = create_rabbit_channel()
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type=exchange_type)
    channel.queue_declare(queue=queue,
                          durable=True)
    channel.queue_bind(queue=queue,
                       exchange=exchange_name,
                       routing_key=routing_key)
    return channel
    
def publish_message(queue_id: int, message: str):
    if not queue_id in QUEUE_PARAMS_MAPPING.keys():
        raise ValueError(f'Wrong queue_id {queue_id} passed in.')
    
    channel = get_channel(exchange_name=QUEUE_PARAMS_MAPPING[queue_id]['exchange_name'],
                          exchange_type=QUEUE_PARAMS_MAPPING[queue_id]['exchange_type'],
                          queue=QUEUE_PARAMS_MAPPING[queue_id]['queue_name'],
                          routing_key=QUEUE_PARAMS_MAPPING[queue_id]['routing_key'])
    
    channel.basic_publish(exchange=QUEUE_PARAMS_MAPPING[queue_id]['exchange_name'],
                          routing_key=QUEUE_PARAMS_MAPPING[queue_id]['routing_key'],
                          body=message)
    
    print(f'func: {sys._getframe().f_code.co_name}\n\t'
          f'Sent message to queue {QUEUE_NAME_MAPPING[queue_id]}')
    
    channel.close()

def send_email(email: str, message: str):
    """Imagine we send an email."""
    print(f'"{message}"')
    print(f'func: {sys._getframe().f_code.co_name}\n\t'
              f'notification was sent to {email}')
