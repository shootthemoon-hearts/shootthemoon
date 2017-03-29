from channels.generic.websockets import JsonWebsocketConsumer
from channels.generic import BaseConsumer
from game_app.event_handler_generics import key_is_key_event_handler
from game_app.event_handler_generics import value_is_key_event_handler

from game_app.models.game import Game
from game_app.models.player import Player
from game_app.rules import game as game_rules

def receive_pass_cards(content):
    cards = content['received_cards']
    turn_id = content['turn_id']
    player = Player.objects.get(id=content['player_id'])
    game = player.enrolled_game
    game_rules.pass_cards_selected(game, cards, player, turn_id)
    
def receive_trick_discard(content):
    cards = content['received_cards']
    turn_id = content['turn_id']
    player = Player.objects.get(id=content['player_id'])
    game = player.enrolled_game
    game_rules.trick_cards_selected(game, cards, player, turn_id)
    
def start_game(content):
    game = Game.objects.get(id=content['game_id'])
    game_rules.start(game)


player_event_manager = key_is_key_event_handler()
player_event_manager.register_handler('pass_cards_selected', receive_pass_cards)
player_event_manager.register_handler('trick_card_selected', receive_trick_discard)

command_event_manager = value_is_key_event_handler('command','command_args')
command_event_manager.register_handler('start_game', start_game)
command_event_manager.register_handler('pass_cards_selected', receive_pass_cards)
command_event_manager.register_handler('trick_card_selected', receive_trick_discard)


class GamePlayerEventConsumer(JsonWebsocketConsumer):
    http_user = True    
    def receive(self, content, multiplexer, **kwargs):
        player = Player.objects.get(channel=multiplexer.reply_channel.name)
        #temporary, "this kit needs to change"
        key = list(content.keys())[0] #presuming 1 key
        content[key]['player_id']=player.id
        player_event_manager.act_on(content)    


class GameCommandEventConsumer(BaseConsumer):
        
    method_mapping = {
        "game_command": "act_on_command",
    }
    
    def act_on_command(self, message, **kwargs):
        command_event_manager.act_on(message.content)

        