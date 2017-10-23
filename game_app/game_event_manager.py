from channels.generic.websockets import JsonWebsocketConsumer
from channels.generic import BaseConsumer
from game_app.event_handler_generics import key_is_key_event_handler
from game_app.event_handler_generics import value_is_key_event_handler

from game_app.models.game import Game
from game_app.models.player import Player
from game_app.rules import game as game_rules
from game_app.rules import pass_round
from game_app.rules import trick_turn
from game_app.card import Card

from django.utils import timezone

def receive_pass_cards(content):
    cards_str = content['received_cards']
    turn_id = content['turn_id']
    player_id = content['player_id']
    passed_cards = Card.list_from_str_list(cards_str)
    pass_round.received_passed_cards(passed_cards, player_id, turn_id)

def receive_trick_discard(content):
    # Get the move time first so the player isn't punished by slow server
    # processing,
    move_time = timezone.now()
    cards = content['received_cards']
    turn_id = content['turn_id']
    player_id = content['player_id']
    # The assumption is that the player can only select one card on their turn
    # for the trick.
    discard = Card.list_from_str_list(cards)[0]
    trick_turn.card_discarded(discard, player_id, turn_id, move_time)

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
        'game_command': 'act_on_command',
    }
    
    def act_on_command(self, message, **kwargs):
        command_event_manager.act_on(message.content)

        