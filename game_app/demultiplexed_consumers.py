from channels.generic.websockets import WebsocketDemultiplexer
from game_app.match_maker_event_manager import MatchmakePlayerEventConsumer
from game_app.game_event_manager import GamePlayerEventConsumer
from game_app.metric_event_manager import MetricEventConsumer 


#this makes value_is_key_event
class Demultiplexer(WebsocketDemultiplexer): 
    
    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "matchmake": MatchmakePlayerEventConsumer,
        "game": GamePlayerEventConsumer,
        "metric": MetricEventConsumer,     
    }
    
    @staticmethod
    def channel_names():
        return "websocket.receive"
    
    
    
    