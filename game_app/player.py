class Player():
    '''Represents a player of the game

    Attributes:
        channel: The django channel used to communicate with the client
    '''
    def __init__(self, channel):
        '''Constructor

        Args:
            channel: The django channel used to communicate with the client
        '''
        self.channel = channel
        self.hand = []
        self.pass_hand = []
        self.position = None
        self.hand_points = 0
        self.game_points = 0
        
        self.accounts = None
        
        ''' these are supposed to get sent to update the account in some way after the game '''
        self.new_elo = None
        self.new_rank = None
        self.new_rank_progress = None
        self.place_this_game = None
        
        
        
        