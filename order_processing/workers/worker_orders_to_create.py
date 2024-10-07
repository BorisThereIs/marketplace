import json
import os
import sys

from dotenv import load_dotenv
load_dotenv()
sys.path.insert(1, os.environ.get('PROJECT_ROOT_DIR',
                                  '/home/superuser/practice/projects/marketplace'))

from sqlalchemy import select

from order_processing.consts import (EXCHANGE_ORDERS_TO_CREATE, QUEUE_NAME_MAPPING, QUEUE_ORDERS_TO_CREATE,
                      QUEUE_ORDERS_TO_PROCESS, ROUTING_KEY_ORDERS_TO_CREATE)
from consts import ORDER_STATUS_PENDING_VALIDATION
from models.product import Product
import pydantic_models
from utils import get_db_session
from order_processing.utils import get_channel, publish_message
from models.order import Order, OrderLine, ShippingAddress
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


def create_order(channel: BlockingChannel, method: Basic.Deliver, properties, body: bytes):
    session = get_db_session(expire_on_commit=False, echo=True)
    order_as_dict = json.loads(body.decode())
    order_model = pydantic_models.Order(**order_as_dict)
    order = Order(status_id=ORDER_STATUS_PENDING_VALIDATION,
                  user_id=order_model.user_id,
                  shipping_address_id=(
                      order_model.shipping_address_id if order_model.shipping_address_id else (
                          session.scalar(
                          select(ShippingAddress.id)
                          .where(ShippingAddress.user_id == order_model.user_id)
                          )
                      )
                  ),
                  total_value=0)
    order_lines = []
    
    for order_line_dict in order_model.order_lines:
        order_line = OrderLine(order=order,
                               product_id=order_line_dict.get('product_id'),
                               quantity=order_line_dict.get('quantity', 1),
                               value=(session.scalar(
                                   select(Product.price)
                                   .where(Product.id == order_line_dict.get('product_id'))
                                   ) * order_line_dict.get('quantity', 1)
                                )
                            )
        order.total_value += order_line.value # type: ignore
        order_lines.append(order_line)
    
    try:
        session.add_all([order, *order_lines])
        session.commit()

        print(f'func: {sys._getframe().f_code.co_name}\n\t'
              f'created an order {order.id}')

        publish_message(queue_id=QUEUE_ORDERS_TO_PROCESS,
                        message=json.dumps({'order_id': order.id}))
    except (SQLAlchemyError, DBAPIError) as e:
        session.rollback()
        print(e)

    session.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)

def consume_orders_to_create():
    channel = get_channel(exchange_name=EXCHANGE_ORDERS_TO_CREATE,
                          exchange_type='direct',
                          queue=QUEUE_NAME_MAPPING[QUEUE_ORDERS_TO_CREATE],
                          routing_key=ROUTING_KEY_ORDERS_TO_CREATE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME_MAPPING[QUEUE_ORDERS_TO_CREATE],
                          on_message_callback=create_order)
    
    print(f'func: {sys._getframe().f_code.co_name}\n\tConsumer started.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        consume_orders_to_create()
    except KeyboardInterrupt as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
