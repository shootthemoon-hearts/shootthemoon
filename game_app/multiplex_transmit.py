from json import dumps

def transmit(stream,channel,data):
    packet = {'stream':stream,
              'payload':data}
    channel.send({'text': dumps(packet)})   
    
def game_transmit(channel,data):
    transmit('game',channel,data)
    
def matchmake_transmit(channel,data):
    transmit('matchmake',channel,data)