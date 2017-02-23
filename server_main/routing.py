from channels.routing import route, route_class
from game_app.consumers import ws_add
from game_app.consumers import ws_disconnect
from game_app.demultiplexed_consumers import Demultiplexer

channel_routing = [
    route("websocket.connect", ws_add),
    route_class(Demultiplexer),
    route("websocket.disconnect", ws_disconnect),
]
