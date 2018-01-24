from channels.routing import route

from messaging.consumers import message_connect
from messaging.consumers import message_consumer

channel_routing = [
    route('websocket.connect', message_connect),
    route('websocket.receive', message_consumer),
]
