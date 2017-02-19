from channels.generic.websockets import JsonWebsocketConsumer

class metricEventData():
    user_id = 0
    game_id = 0
    turn_id = 0
    action_type = "none"
    cards = ""

class MetricEventConsumer(JsonWebsocketConsumer):
    
    http_user = True
    
    def receive(self, content, multiplexer, **kwargs):
        multiplexer.send({"metric_message": "fuck"}) 
        
