import datetime

from channels import Group
from channels import Channel
from django.db import transaction

from game_app.card import Card
from game_app.models.game_round import GameRound
from game_app.multiplex_transmit import game_transmit

from . import game_round as grrz
from . import pass_round as prrz
from . import trick_turn as ttrz
from . import ranking as rrz

POINTS_TO_WIN = 100

def setup(g,players):
    g.group_channel = "game_%s" % g.id
    g.save()
    for player in players:
        add_player(g,player,g.group_channel)
    send_group_the_phase(g,'BEFORE_GAME')
    g.date = datetime.datetime.now()

def add_player(g, player,group):
    game_transmit(Channel(player.channel),{'id':str(g.id)})
    player.enrolled_game = g
    player.position = len(g.player_set.all()) #no -1 because didn't save yet
    game_transmit(Channel(player.channel),{"player_pos":player.position})
    player.save()
    Group(group).add(Channel(player.channel))
    print ('Game', g.id, 'has', len(g.player_set.all()), 'players')

def start(g):
    g.active = True
    game_transmit(Group(g.group_channel),{"enter_room": None})
    g.save()
    add_round(g)
    
def send_group_the_phase(g,phase):
    game_transmit(Group(g.group_channel),{"game_phase": phase})
        
def add_round(g):
    send_players_score(g)
    game_over = check_winning_conditions(g)
    if not game_over:
        gr = GameRound()
        grrz.setup(gr,g,len(g.gameround_set.all()))
        grrz.start(gr)

def pass_cards_selected(g, cards_str, player, turn_id):
    cards = Card.list_from_str_list(cards_str)
    prrz.received_passed_cards(g.gameround_set.get(active=True).passround,player,cards,turn_id)

def trick_cards_selected(g,cards_str, player, turn_id):
    cards = Card.list_from_str_list(cards_str)
    card = cards[0]
    ttrz.card_discarded(g.gameround_set.get(active=True).trickturn_set.get(active=True),player,card,turn_id)
    
def send_players_score(g):
    '''Sends a message to each player telling them the scores -- only
    updates after each hand'''
    score_list = []
    for player in g.player_set.all():
        score_list.append(str(player.game_points))
    game_transmit(Group(g.group_channel),{"scores": {"player": player.position, "score_list": score_list}})

def check_winning_conditions(g):
    for player in g.player_set.all():
        if player.game_points >= POINTS_TO_WIN:
            finish(g)
            return True
    
    return False

            
def how_people_placed(g):
        ''' saves the place each player got in each players' place_this_game
        attribute. '''
        player_list = [player for player in g.player_set.all()]
        player_list.sort(key=lambda player: (player.game_points + player.position))

        for i, player in enumerate(player_list):
            player.place_this_game = i
            player.save()
    
            

def finish(g):
    how_people_placed(g)
    rrz.elo_calculation(g)
    rrz.rank_calculation(g)
    g.active = False
    g.save()

        
