from game_app.models import Game
from game_app.models import MatchMakingQueue
from channels import Channel

def join_queue(queue_name,player):
    
    if player.active_queue != None:
        multiple_leave_queue_with_trust(player.active_queue,[player])
        
    queue = MatchMakingQueue.objects.get(name=queue_name)
    queue.total_players += 1
    queue.save()
    
    player.active_queue = queue
    player.save()
    
    if queue.total_players >= 4:
        players_to_join_game = list(queue.player_set.all()[0:4])
        multiple_leave_queue_with_trust(queue_name,players_to_join_game)
        new_game = Game()
        new_game.setup(players_to_join_game)     
        Channel('game_command').send({'command':'start_game','game_id':new_game.id})
    
        
def multiple_leave_queue_with_trust(queue_name,players):
    queue = MatchMakingQueue.objects.get(name=queue_name)
    queue.total_players -= len(players)
    queue.save()
    for player in players:
        player.active_queue = None
        player.save()
        

def leave_queue_with_check(queue_name,player):
    if player.active_queue == queue_name:
        multiple_leave_queue_with_trust(queue_name,[player])
        
