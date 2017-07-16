import json
from django.shortcuts import render

from game_app.models.game import Game
from game_app.models.player import Player
from game_app.models.account import Account

GAME_STR = 'game_history'
ELO_STR = 'elo'
PLACEMENT_STR = 'Placement'
DATE_PLAYED = 'Date Played'

def index(request):
    context = {}

    game_json = _get_game_history_json(request)
    context[GAME_STR] = game_json
    
    elo = _get_elo_json(request)
    context[ELO_STR] = elo
    return render(request, 'stats/index.html', context=context)

def _get_game_history_json(request):

    games_played = Game.objects.filter(player__user=request.user, active=False).distinct()

    json_game_list = []
    header = [DATE_PLAYED, PLACEMENT_STR]
    for game in games_played:
        # TODO: Since the same user can sit in multiple seats in a game, it is
        # possible for this query to return multiple players
        # For the time being, just return the first player found
        player = Player.objects.filter(user=request.user,
                                       enrolled_game__active=False,
                                       enrolled_game=game)[0]

        date_played = game.date.timestamp()
        # Add 1 so it's not 0 indexed
        place = player.place_this_game + 1
        json_game_list.append([date_played, place])
        
    json_game_list.sort(key=lambda x: x[0])
    json_game_list.insert(0, header)
    return json.dumps(json_game_list)

def _get_elo_json(request):
    account = Account.objects.get(user=request.user)
    elo = account.elo
    
    return elo
