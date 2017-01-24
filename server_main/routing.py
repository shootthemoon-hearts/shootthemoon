from channels.routing import route
from game_app.consumers import ws_add
from game_app.consumers import ws_message
from game_app.consumers import ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
