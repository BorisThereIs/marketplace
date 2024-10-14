import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(1, os.environ['PROJECT_ROOT_DIR'])

from sqlalchemy import select

from order_processing.consts import QUEUE_USER_NOTIFICATIONS
from models.user import User
from utils import get_db_session
from order_processing.utils import send_email, consume_messages
from models.order import Order
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


def send_notification(channel: BlockingChannel, method: Basic.Deliver, properties, body: bytes):
    """Suppose it notifies a user via their email."""
    session = get_db_session(expire_on_commit=False, echo=True)
    message = json.loads(body.decode())
    order_id = message.get('order_id')
    user_data = (session.execute(select(Order.user_id, 
                                   User.first_name, 
                                   User.last_name,
                                   User.email)
                                   .join(Order.user)
                                   .where(Order.id == order_id))
                                   .first())
    notification_message = (
        f'Dear {user_data.first_name} {user_data.last_name},\n'
        f'status of your order {order_id} has been changed from '
        f'"{message.get("prev_status")}" to "{message.get("new_status")}".'
    )

    try:
        send_email(user_data.email, notification_message)
    except Exception as e:
        print(e)

    session.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)

def consume_user_notifications() -> None:
    consume_messages(QUEUE_USER_NOTIFICATIONS, send_notification)

if __name__ == '__main__':
    try:
        consume_user_notifications()
    except KeyboardInterrupt as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
