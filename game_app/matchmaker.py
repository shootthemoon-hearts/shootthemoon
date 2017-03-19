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
        new_game = Game()
        new_game.save()
        players_to_join_game = list(queue.player_set.all()[0:4])
        multiple_leave_queue_with_trust(queue_name,players_to_join_game)
        
        seat_count = 0
        for player_to_join_game in players_to_join_game:
            player_to_join_game.active_game = new_game
            player_to_join_game.seat = seat_count
            player_to_join_game.save()
            seat_count += 1
        
        Channel('game_command').send({})
    
        
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
        
