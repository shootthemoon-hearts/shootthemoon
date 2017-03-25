from json import dumps

def slampig(stream,channel,data):
    packet = {'stream':stream,
              'payload':data}
    channel.send({'text': dumps(packet)})   
    
def game_transmit(channel,data):
    slampig('game',channel,data)
    
def matchmake_transmit(channel,data):
    slampig('matchmake',channel,data)