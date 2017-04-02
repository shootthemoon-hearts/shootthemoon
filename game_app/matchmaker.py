from game_app.models import Game
from game_app.models import MatchMakingQueue
from channels import Channel
from game_app.rules import game as game_rules

def join_queue(queue_name,player):
    
    if player.enrolled_queue != None:
        multiple_leave_queue_with_trust(player.enrolled_queue,[player])
        
    queue = MatchMakingQueue.objects.get(name=queue_name)
    queue.total_players += 1
    queue.save()
    
    player.enrolled_queue = queue
    player.save()
    
    if queue.total_players >= 4:
        players_to_join_game = list(queue.player_set.all()[0:4])
        multiple_leave_queue_with_trust(queue_name,players_to_join_game)
        new_game = Game()
        new_game.save()
        game_rules.setup(new_game,players_to_join_game)     
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
        
