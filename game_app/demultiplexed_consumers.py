from channels.generic.websockets import WebsocketDemultiplexer
from game_app.match_maker_event_manager import MatchmakeEventConsumer
from game_app.game_event_manager import GameEventConsumer
from game_app.metric_event_manager import MetricEventConsumer 

class Demultiplexer(WebsocketDemultiplexer):
    
    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "matchmake": MatchmakeEventConsumer,
        "game": GameEventConsumer,
        "metric": MetricEventConsumer,     
    }
    
    @staticmethod
    def channel_names():
        return "websocket.receive"
    
    
    
    