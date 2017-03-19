from channels.generic.websockets import JsonWebsocketConsumer
from json import dumps
from game_app.event_handler_generics import key_is_key_event_handler
from game_app.models import Player
from game_app.models import MatchMakingQueue
from game_app import matchmaker

player_event_manager = key_is_key_event_handler()
player_event_manager.register_handler('join', matchmaker.join_queue)
player_event_manager.register_handler('leave',matchmaker.leave_queue_with_check)

MatchMakingQueue.objects.all().delete()
queue = MatchMakingQueue()
queue.total_players = 0;
queue.name = 'hanyuu'
queue.save()

class MatchmakePlayerEventConsumer(JsonWebsocketConsumer):
    http_user = True    
    def receive(self, content, multiplexer, **kwargs):
        #we should get player specific game object here and pass it into act_on
        player =  Player()
        player.channel = multiplexer.reply_channel.name
                
        player_event_manager.act_on(content,player)

def transmit(channel,data):
    packet = {'stream':'matchmake',
              'payload':data}
    channel.send({'text': dumps(packet)})
 