import json
from django.shortcuts import render

from game_app.models.game import Game
from game_app.models.player import Player
from game_app.models.account import Account

GAME_STR = 'game_history'
ELO_STR = 'elo'
RANK_STR = 'rank'
PLACEMENT_STR = 'Placement'
DATE_PLAYED = 'Date Played'

def index(request):
    context = {}

    game_json = _get_game_history_json(request)
    context[GAME_STR] = game_json
    
    elo = _get_elo_json(request)
    rank = _get_rank_json(request)
    context[ELO_STR] = elo
    context[RANK_STR] = rank
    return render(request, 'stats/index.html', context=context)

def _get_game_history_json(request):

    games_played = Game.objects.filter(player__user=request.user, active=False).distinct()

    json_game_list = []
    for game in games_played:
        json_game_dict = {}
        # TODO: Since the same user can sit in multiple seats in a game, this 
        # next part is hardcoded.
        player = Player.objects.filter(user=request.user, enrolled_game__active=False, enrolled_game=game)[0]

        # Add 1 so it's not 0 indexed
        json_game_dict[PLACEMENT_STR] = player.place_this_game + 1
        json_game_dict[DATE_PLAYED] = str(game.date)
        json_game_list.append(json_game_dict)
        
    return json.dumps(json_game_list)

def _get_elo_json(request):
    account = Account.objects.get(user=request.user)
    elo = account.elo
    
    return elo

def _get_rank_json(request):
    account = Account.objects.get(user=request.user)
    rank = account.rank
    
    return rank
