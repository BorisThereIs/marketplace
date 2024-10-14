import os
from typing import Any, Dict, List


ORDER_STATUS_PENDING_VALIDATION = 1
ORDER_STATUS_PENDING_APPROVAL = 2
ORDER_STATUS_PENDING_FULFILLMENT = 3
ORDER_STATUS_FULFILLED = 4
ORDER_STATUS_CANCELED = 5
ORDER_STATUS_ON_HOLD = 6

ORDER_STATUS_NAME_MAPPING = {
    ORDER_STATUS_PENDING_VALIDATION: 'Pending Validation',
    ORDER_STATUS_PENDING_APPROVAL: 'Pending Approval',
    ORDER_STATUS_PENDING_FULFILLMENT: 'Pending Fulfillment',
    ORDER_STATUS_FULFILLED: 'Fulfilled',
    ORDER_STATUS_CANCELED: 'Canceled',
    ORDER_STATUS_ON_HOLD: 'On Hold',
}

APP_COMPONENTS_TO_RUN_AS_SEPARATE_PROCESS: List[Dict[str, Any]] = [
    {
        'callable': 'uvicorn.run',
        'kwargs': {
            'app': 'main:app',
            'app_dir': f'{os.environ.get("PROJECT_ROOT_DIR", ".")}/api',
            'host': '0.0.0.0',
            'port': 8000,
        },
    },
    {
        'callable': 'order_processing.workers.worker_orders_to_create.consume_orders_to_create',
    },
    {
        'callable': 'order_processing.workers.worker_orders_to_process.consume_orders_to_process',
    },
    {
        'callable': 'order_processing.workers.worker_user_notifications.consume_user_notifications',
    },
]