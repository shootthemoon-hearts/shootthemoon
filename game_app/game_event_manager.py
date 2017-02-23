from channels.generic.websockets import JsonWebsocketConsumer
from json import dumps
from game_app.event_handler_generics import key_is_key_event_handler

event_manager = key_is_key_event_handler()

class GameEventConsumer(JsonWebsocketConsumer):
    http_user = True    
    def receive(self, content, multiplexer, **kwargs):
        #we should get player specific game object here and pass it into act_on
        event_manager.act_on(content, multiplexer.reply_channel)

def transmit(channel,data):
    packet = {'stream':'game',
              'payload':data}
    channel.send({'text': dumps(packet)})
        