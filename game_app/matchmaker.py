from channels import Channel
from django.db import transaction
from game_app.models import Game
from game_app.models import MatchMakingQueue
from game_app.rules import game as game_rules

MAX_PLAYER_COUNT = 4

def join_queue(queue_name,player):
    
    if player.enrolled_queue != None:
        multiple_leave_queue_with_trust(player.enrolled_queue,[player])
        
    queue = MatchMakingQueue.objects.get(name=queue_name)
    queue.total_players += 1
    queue.save()
    
    player.enrolled_queue = queue
    player.save()
    
    if queue.total_players >= MAX_PLAYER_COUNT:
        with transaction.atomic():
            players_to_join_game = list(queue.player_set.select_for_update().all()[0:MAX_PLAYER_COUNT])
            multiple_leave_queue_with_trust(queue_name, players_to_join_game)
            new_game = Game()
            game_rules.setup(new_game, players_to_join_game)
        Channel('game_command').send({'command':'start_game','command_args':{'game_id':new_game.id}})
    
        
def multiple_leave_queue_with_trust(queue_name,players):
    queue = MatchMakingQueue.objects.get(name=queue_name)
    queue.total_players -= len(players)
    queue.save()
    for player in players:
        player.enrolled_queue = None
        player.save()
        

def leave_queue_with_check(queue_name,player):
    if player.enrolled_queue == queue_name:
        multiple_leave_queue_with_trust(queue_name,[player])
        
