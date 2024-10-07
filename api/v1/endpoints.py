from fastapi import APIRouter
from sqlalchemy import select

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(1, os.environ.get('PROJECT_ROOT_DIR',
                                  '/home/superuser/practice/projects/marketplace'))

from models.order import Order
from utils import get_db_session
from order_processing.utils import publish_message
import pydantic_models
from order_processing.consts import QUEUE_ORDERS_TO_CREATE


router = APIRouter(prefix='/api/v1')

@router.get('/orders')
async def get_orders():
    session = get_db_session()
    orders = session.scalars(select(Order)).all()
    return orders

@router.get('/orders/{order_id}')
async def get_order(order_id: int):
    session = get_db_session()
    order = session.scalars(select(Order).where(Order.id == order_id)).first()
    return order

@router.post('/orders')
async def create_order(order_to_create: pydantic_models.Order):
    order_as_json = order_to_create.model_dump_json()
    publish_message(QUEUE_ORDERS_TO_CREATE, order_as_json)
    return order_as_json
