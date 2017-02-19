from channels.generic.websockets import WebsocketDemultiplexer, JsonWebsocketConsumer
from game_app.match_maker_event_manager import MatchmakeEventConsumer
from game_app.game_event_manager import GameEventConsumer

        
class MetricEventConsumer(JsonWebsocketConsumer):
    def receive(self, content, multiplexer, **kwargs):
        multiplexer.send({"metric_message": content})        
        
class DefaultEventConsumer(JsonWebsocketConsumer):
    def receive(self, content, multiplexer=None, **kwargs):
        multiplexer.send({"default_message": content})  


class Demultiplexer(WebsocketDemultiplexer):
    
    # Wire your JSON consumers here: {stream_name : consumer}
    consumers = {
        "matchmake": MatchmakeEventConsumer,
        "game": GameEventConsumer,
        "metric": MetricEventConsumer,
        "other": DefaultEventConsumer,        
    }
    
    @staticmethod
    def channel_names():
        return "websocket.receive"
    
    
    
    
    