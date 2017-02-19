from channels.generic.websockets import JsonWebsocketConsumer

class matchEventData():
    user_id = 0
    game_session = 0
    game_type = ""
    lobby = ""
    rank = ""
    

class MatchmakeEventConsumer(JsonWebsocketConsumer):
    
    http_user = True
    
    def receive(self, content, multiplexer, **kwargs):
        multiplexer.send({"matchmaker_message": content})
        
        
        
        """      
        if game_session >= 0:
            #send back, join game session
            pass
        else:
            pass #match = match_for_player(game_type,lobby,rank);
            if 0 == NULL:
                pass #save_player(game_type,lobby,rank)
                pass #wait_time = get_wait_time(game_type,lobby,rank)
                #send back wait time
            else:
                #send back, join game session
                pass
                """