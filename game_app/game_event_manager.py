from channels.generic.websockets import JsonWebsocketConsumer
from game_app import event_manager

class gameEventData():
    user_id = 0
    game_id = 0
    turn_id = 0
    action_type = "none"
    cards = ""

class GameEventConsumer(JsonWebsocketConsumer):
    
    http_user = True
    
    def receive(self, content, multiplexer, **kwargs):
        event_manager.event_received(content, multiplexer.reply_channel);
        
        