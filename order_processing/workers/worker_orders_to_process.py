import json
import os
import sys

from dotenv import load_dotenv
load_dotenv()
sys.path.insert(1, os.environ.get('PROJECT_ROOT_DIR',
                                  '/home/superuser/practice/projects/marketplace'))

from sqlalchemy import select

from order_processing.consts import (EXCHANGE_ORDERS_TO_PROCESS, QUEUE_NAME_MAPPING, QUEUE_ORDERS_TO_PROCESS,
                      QUEUE_USER_NOTIFICATIONS, ROUTING_KEY_ORDERS_TO_PROCESS)
from consts import ORDER_STATUS_NAME_MAPPING, ORDER_STATUS_PENDING_FULFILLMENT
from utils import get_db_session
from order_processing.utils import get_channel, publish_message
from models.order import Order
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


def process_order(channel: BlockingChannel, method: Basic.Deliver, properties, body: bytes):
    """It's an oversimplified order processing that implies some validation and status change."""
    session = get_db_session(expire_on_commit=False, echo=True)
    order_id = json.loads(body.decode()).get('order_id')
    order = session.scalars(select(Order).where(Order.id == order_id)).first()
    is_valid = True
    message_to_send = {}
    message_to_send['order_id'] = order.id
    message_to_send['prev_status'] = ORDER_STATUS_NAME_MAPPING[order.status_id]

    # some order-related validation happens here.
    # next order status might depend on both a current status and the validation results.

    if is_valid:
        order.status_id = ORDER_STATUS_PENDING_FULFILLMENT

    try:
        session.add_all([order,])
        session.commit()

        print(f'func: {sys._getframe().f_code.co_name}\n\t'
              f'processed an order {order.id}')
        
        message_to_send['new_status'] = ORDER_STATUS_NAME_MAPPING[ORDER_STATUS_PENDING_FULFILLMENT]

        publish_message(queue_id=QUEUE_USER_NOTIFICATIONS,
                        message=json.dumps(message_to_send))
    except (SQLAlchemyError, DBAPIError) as e:
        session.rollback()
        print(e)

    session.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)

def consume_orders_to_process():
    channel = get_channel(exchange_name=EXCHANGE_ORDERS_TO_PROCESS,
                          exchange_type='direct',
                          queue=QUEUE_NAME_MAPPING[QUEUE_ORDERS_TO_PROCESS],
                          routing_key=ROUTING_KEY_ORDERS_TO_PROCESS)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME_MAPPING[QUEUE_ORDERS_TO_PROCESS],
                          on_message_callback=process_order)
    
    print(f'func: {sys._getframe().f_code.co_name}\n\tConsumer started.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        consume_orders_to_process()
    except KeyboardInterrupt as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
