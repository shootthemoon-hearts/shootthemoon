class Game():

    def __init__(self, channel, ID):
        self.channel = channel
        self.players = 0
        self.gameID = ID

    def isFull(self):
        return self.players >= 4

    def addPlayer(self, channel):
        channel.send({'text': '{"id":' + str(self.gameID) + '}'})
        self.players += 1
        print ('Game', self.gameID, 'has', self.players, 'players')
    
