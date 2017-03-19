from channels.generic.websockets import JsonWebsocketConsumer
from channels.generic import BaseConsumer
from json import dumps
from game_app.event_handler_generics import key_is_key_event_handler
from game_app.game import Game
from game_app.game import Game

player_event_manager = key_is_key_event_handler()
#player_event_manager.register_handler('pass_cards_selected', pass_cards_selected)
#player_event_manager.register_handler('trick_card_selected', trick_cards_selected)



command_event_manager = key_is_key_event_handler()




class GamePlayerEventConsumer(JsonWebsocketConsumer):
    http_user = True    
    def receive(self, content, multiplexer, **kwargs):
        #we should get player specific game object here and pass it into act_on
        player_event_manager.act_on(content, multiplexer.reply_channel)
        
def multiplex_transmit(channel,data):
    packet = {'stream':'game',
              'payload':data}
    channel.send({'text': dumps(packet)})        



class GameCommandEventConsumer(BaseConsumer):
    method_mapping = {
        "game_command": "method_name",
    }
    def method_name(self, message, **kwargs):
        pass

        