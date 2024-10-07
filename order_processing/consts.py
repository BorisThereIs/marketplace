QUEUE_ORDERS_TO_CREATE = 0
QUEUE_ORDERS_TO_PROCESS = 1
QUEUE_USER_NOTIFICATIONS = 2

QUEUE_NAME_MAPPING = {
    QUEUE_ORDERS_TO_CREATE: 'queue_orders_to_create',
    QUEUE_ORDERS_TO_PROCESS: 'queue_orders_to_process',
    QUEUE_USER_NOTIFICATIONS: 'queue_user_notifications',
}
EXCHANGE_ORDERS_TO_CREATE = 'exchange_orders_to_create'
EXCHANGE_ORDERS_TO_PROCESS = 'exchange_orders_to_process'
EXCHANGE_USER_NOTIFICATIONS = 'exchange_user_notification'

ROUTING_KEY_ORDERS_TO_CREATE = 'orders_to_create'
ROUTING_KEY_ORDERS_TO_PROCESS = 'orders_to_process'
ROUTING_KEY_USER_NOTIFICATIONS = 'user_notifications'

QUEUE_PARAMS_MAPPING = {
    QUEUE_ORDERS_TO_CREATE: {
        'exchange_name': EXCHANGE_ORDERS_TO_CREATE,
        'exchange_type': 'direct',
        'queue_name': QUEUE_NAME_MAPPING[QUEUE_ORDERS_TO_CREATE],
        'routing_key': ROUTING_KEY_ORDERS_TO_CREATE,
    },
    QUEUE_ORDERS_TO_PROCESS: {
        'exchange_name': EXCHANGE_ORDERS_TO_PROCESS,
        'exchange_type': 'direct',
        'queue_name': QUEUE_NAME_MAPPING[QUEUE_ORDERS_TO_PROCESS],
        'routing_key': ROUTING_KEY_ORDERS_TO_PROCESS,
    },
    QUEUE_USER_NOTIFICATIONS: {
        'exchange_name': EXCHANGE_USER_NOTIFICATIONS,
        'exchange_type': 'direct',
        'queue_name': QUEUE_NAME_MAPPING[QUEUE_USER_NOTIFICATIONS],
        'routing_key': ROUTING_KEY_USER_NOTIFICATIONS,
    },
}
