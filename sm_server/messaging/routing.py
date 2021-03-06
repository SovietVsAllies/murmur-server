from channels import route

from messaging.consumers import message_connect, message_consumer, message_disconnect

channel_routing = [
    route('websocket.connect', message_connect, path=r'^/message/$'),
    route('websocket.receive', message_consumer, path=r'^/message/$'),
    route('websocket.disconnect', message_disconnect, path=r'^/message/$'),
]
