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
        self.new_elo = 0
        self.new_rank = 0
        self.new_rank_progress = 0