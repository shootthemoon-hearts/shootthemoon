from channels.routing import route
from heartsgame.consumers import ws_add
from heartsgame.consumers import ws_message
from heartsgame.consumers import ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
