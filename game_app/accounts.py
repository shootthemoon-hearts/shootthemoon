class Account():
    ''' has to do with database info we have on the user'''
    def __init__(self):
        '''Constructor'''
        
        ''' these will be database-stored values, no database yet tho. '''
        self.username = None
        self.elo = None
        self.rank = None
        self.rank_points = None
        self.games_played = None