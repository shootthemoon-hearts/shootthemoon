from channels.routing import route, route_class, null_consumer
from game_app.consumers import ws_add
from game_app.consumers import ws_disconnect
from game_app.demultiplexed_consumers import Demultiplexer
from game_app.game_event_manager import GameCommandEventConsumer

channel_routing = [
    route_class(GameCommandEventConsumer),
    route("websocket.connect", ws_add),
    route_class(Demultiplexer),
    route("websocket.disconnect", ws_disconnect),
    route("null",null_consumer),
]
