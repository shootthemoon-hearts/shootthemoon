from channels.generic.websockets import JsonWebsocketConsumer
from channels.generic import BaseConsumer
from game_app.event_handler_generics import key_is_key_event_handler
from game_app.event_handler_generics import value_is_key_event_handler

from game_app.models.game import Game


def receive_pass_cards(game,content,channel):
    game.pass_cards_selected(content,channel)
    
def receive_trick_discard(game,content,channel):
    game.trick_cards_selected(game,content,channel)
    
def start_game(content):
    game = Game.objects.get(id=content['game_id'])
    game.start()

player_event_manager = key_is_key_event_handler()
player_event_manager.register_handler('pass_cards_selected', receive_pass_cards)
player_event_manager.register_handler('trick_card_selected', receive_trick_discard)

command_event_manager = value_is_key_event_handler('command','game_id')
command_event_manager.register_handler('start_game', start_game)


class GamePlayerEventConsumer(JsonWebsocketConsumer):
    http_user = True    
    def receive(self, content, multiplexer, **kwargs):
        #we should get player specific game object here and pass it into act_on
        player_event_manager.act_on(content, multiplexer.reply_channel)    



class GameCommandEventConsumer(BaseConsumer):
    method_mapping = {
        "game_command": "act_on_command",
    }
    def act_on_command(self, message, **kwargs):
        command_event_manager.act_on(message.content)

        