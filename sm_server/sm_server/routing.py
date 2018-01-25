from channels.routing import include

channel_routing = [
    include('messaging.routing.channel_routing')
]
