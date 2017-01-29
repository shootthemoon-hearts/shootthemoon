import logging

class Game():
    '''This class will represent an individual game

    Attributes:
        channel: channel to connect to (honestly this shouldn't be here, if
            anything, this should be the group of channels to communicate 
            with)
        players: The amount of players connected to the game. Cannot be higher
            than MAX_PLAYERS
        gameID: The game's unique identifier
        MAX_PLAYERS: The maximum amount of players that can be connected to 
            this game
    '''
    MAX_PLAYERS = 4

    def __init__(self, channel, ID):
        '''Constructor

        Args:
            channel: channel to connect to (honestly this shouldn't be here, if
                anything, this should be the group of channels to communicate 
                with)
            ID: the unique identifier of the game (should this be passed in 
                as a parameter or should the game itself decide??
        '''
        self.channel = channel
        self.players = 0
        self.gameID = ID

    def isFull(self):
        '''Returns whether or not the game is full'''
        if self.players == MAX_PLAYERS:
            return True
        elif self.players > MAX_PLAYERS:
            logging.warn('The game %s somehow has more players than the maximum',
                    self.gameID)
            return True
        else:
            return False

    def addPlayer(self, channel):
        '''Adds a player to the game

        Args:
            channel: The django channel used to communicate with the player's
                client
        '''
        #TODO: Add the player to the game's group
        channel.send({'text': '{"id":' + str(self.gameID) + '}'})
        self.players += 1
        print ('Game', self.gameID, 'has', self.players, 'players')
    
