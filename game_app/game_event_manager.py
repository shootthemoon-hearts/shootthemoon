from channels.generic.websockets import JsonWebsocketConsumer

class gameEventData():
    user_id = 0
    game_id = 0
    turn_id = 0
    action_type = "none"
    cards = ""

class GameEventConsumer(JsonWebsocketConsumer):
    
    http_user = True
    
    def receive(self, content, multiplexer, **kwargs):
        multiplexer.send({"game_message": "fuck"}) 
        """
        user_id = 0;
        session_id = 0;
        """
        
        #new game request from matchmaker
        #    assign players
        #    get game type, get process for round
        #    send initial seat info and rules for game type
        #    deal to players
        #    set timeout for acks
        #    end game if missing player
        #    
        #
        #
        #
        