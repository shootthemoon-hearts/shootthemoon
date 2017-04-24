import datetime
import logging

from channels import Group
from channels import Channel
from django.db import transaction

from game_app.card import Card
from game_app.models.game_round import GameRound
from game_app.multiplex_transmit import game_transmit
from game_app.rules import game_round
from game_app.rules import pass_round
from game_app.rules import trick_turn
from game_app.rules import ranking

POINTS_TO_WIN = 100

GAME_GROUP_CHANNEL_PREFIX= 'game_'

PHASE_BEFORE_GAME = 'BEFORE_GAME' 

def setup(game, players, delay):
    '''Sets up the game and player database objects. 
    
    This function guarantees a save of the game and player database entries.
    
    Arguments:
        game: the game database entry
        players: a list of the database entries of each player in the game
    '''
    game.group_channel = "%s_%s" % (GAME_GROUP_CHANNEL_PREFIX, game.id)
    game.date = datetime.datetime.now()
    game.save()
    # It's possible this may be the first time this game is getting saved, so 
    # the game needs to get saved before the players get added
    for player in players:
        add_player(game, player, game.group_channel)
    send_group_the_phase(game, PHASE_BEFORE_GAME)
    
    delay_message = {
        'channel':'game_command',
        'delay':delay,
        'content':{
            'command':'start_game',
            'command_args':{
                'game_id': game.id
            }
        }
    }
    Channel('asgi.delay').send(delay_message)

def add_player(game, player, group):
    '''Adds the given player to the given game and group
    
    Arguments:
        game: the game database entry
        player: the player database entry
        group: the group channel to add the player to
    '''
    player.enrolled_game = game
    player.position = len(game.player_set.all()) #no -1 because didn't save yet
    player.save()
    Group(group).add(Channel(player.channel))
    game_transmit(Channel(player.channel), {'enter_room':
        {'id':str(game.id),'player_pos':player.position}})
    logging.info('Game %s has %s players', game.id, 'has', game.player_set.all().count(), 'players')

def start(game):
    '''Starts the game
    
    Arguments:
        game: the game database entry
    '''
    game.active = True
    game.save()
    add_round(game)
    
def send_group_the_phase(game, phase):
    '''Sends each player in the game the current phase
    
    Arguments:
        game: the game database entry
        phase: the current game phase
    '''
    game_transmit(Group(game.group_channel), {"game_phase": phase})
        
def add_round(game):
    '''Adds a new game round to the given game and starts it
    
    Arguments:
        game: the game database entry
    '''
    send_players_score(game)
    game_over = check_winning_conditions(game)
    if not game_over:
        game_round_entry = GameRound()
        game_round.setup(game_round_entry, game, game.gameround_set.all().count())
        game_round.start(game_round_entry)

def pass_cards_selected(game, cards_str, player, turn_id):
    '''Called when a player selects which cards to pass
    
    Arguments:
        game: the game database entry
        cards_str: a string shorthand representing which cards the player chose
            to pass
        player: the database entry for the player who is passing their cards
        turn_id: the id of the current turn
    '''
    cards = Card.list_from_str_list(cards_str)
    pass_round.received_passed_cards(game.gameround_set.get(active=True).passround,player,cards,turn_id)

def trick_cards_selected(game, cards_str, player, turn_id):
    '''Called when a player selects which card to play for the trick turn
    
    Arguments:
        game: the game database entry
        cards_str: a string shorthand representing which cards the player chose
            to pass
        player: the database entry for the player who is passing their cards
        turn_id: the id of the current turn
    '''
    cards = Card.list_from_str_list(cards_str)
    # The assumption is that the player can only select one card on their turn
    # for the trick. 
    card = cards[0]
    trick_turn.card_discarded(game.gameround_set.get(active=True).trickturn_set.get(active=True), player, card, turn_id)
    
def send_players_score(game):
    '''Sends a message to each player telling them the scores 
    
    Note: this is only updated after each hand
    
    Arguments:
        game: the game database entry
    '''
    score_list = []
    for player in game.player_set.all():
        score_list.append(str(player.game_points))
    game_transmit(Group(game.group_channel),
                  {"scores": 
                   {"player": player.position, "score_list": score_list}
                  }
                 )

def check_winning_conditions(game):
    '''Checks if anyone has won the game
    
    Arguments:
        game: the game database entry
        
    Returns:
        Whether or not anyone has won the game
    '''
    for player in game.player_set.all():
        if player.game_points >= POINTS_TO_WIN:
            finish(game)
            return True
    
    return False

            
def save_how_people_placed(game):
    '''Saves the place each player got in each players' place_this_game
    attribute. 
    
    Arguments:
        game: the game database entry
    '''
    with transaction.atomic():
        player_list = list(game.player_set.select_for_update().all())
        # The reason player position is involved in this is to provide a
        # mechanism for tie resolution. This algorithm currently does not allow
        # for draws, so instead it whoever joined the game first as the winner.
        player_list.sort(key=
                         lambda player: (player.game_points + player.position))

        for i, player in enumerate(player_list):
            player.place_this_game = i
            player.save()
    
            

def finish(game):
    '''Saves the game state after someone has won the game.
    
    Arguments:
        game: the game database entry
    '''
    save_how_people_placed(game)
    ranking.elo_calculation(game)
    #TODO: Reimplement rank_calculation
#         ranking.rank_calculation(game)
    game.active = False
    game.save()

        
