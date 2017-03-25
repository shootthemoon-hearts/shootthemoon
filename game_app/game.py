from .accounts import Account
from .round import Round
from .card import Card
from .deck import Deck
from .player import Player
from .trick_turn import TrickTurn
from .pass_round import PassRound
from .game_event_manager import event_manager
from .game_event_manager import transmit
from channels import Group

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
    BEFORE_GAME = 'BEFORE_GAME'
    IN_TRICK = 'IN_TRICK'
    PASS_PHASE = 'PASS_PHASE'
    

    def __init__(self, channel, ID):
        '''Constructor

        Args:
            channel: channel to connect to (honestly this shouldn't be here, if
                anything, this should be the group of channels to communicate 
                with)
            ID: the unique identifier of the game (should this be passed in 
                as a parameter or should the game itself decide??
        '''
        self.rounds = []
        self.channel = channel
        self.players = []
        self.gameID = ID
        self.tricks_this_hand = 0
        self.phase = Game.BEFORE_GAME
        self.tricks = []
        self.game_winner = -1
        self.trick_count = 13 #13 normally
        self.hearts_broken = False
        self.group = Group("game_%s" % ID)
        self.final_scores = []
        
    def add_players_to_group(self, group):
        for player in self.players:
            group.add(player.channel)

    def isFull(self):
        '''Returns whether or not the game is full'''
        if len(self.players) == Game.MAX_PLAYERS:
            return True
        elif len(self.players) > Game.MAX_PLAYERS:
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
        transmit(channel,{'id':str(self.gameID)})
        new_player = Player(channel)
        self.players.append(new_player)
        position = len(self.players) - 1
        new_player.position = position
        transmit(channel,{"player_pos":new_player.position})
        print ('Game', self.gameID, 'has', self.players, 'players')
    
    def clear_hands(self):
        for i in self.players:
            i.hand = []
            i.pass_hand = []
            
    #def clear_tricks(self):
        #self.tricks = []
            
    def reset_hearts_broken(self):
        self.hearts_broken = False
            
    #def clear_tricks(self):
        #self.tricks = []
    
    def setup_game(self):
        '''Sets up the game'''
        self.add_players_to_group(self.group)
        if len(self.rounds) != 0:
            self.clear_hands()
            self.reset_hearts_broken()
            #self.clear_tricks()
        event_manager.register_handler('pass_cards_selected', self.pass_cards_selected)
        event_manager.register_handler('trick_card_selected', self.trick_cards_selected)
        self.phase = Game.BEFORE_GAME
        self.rounds.append(Round(len(self.rounds), self.phase))
        self.tell_round_phase()
        self.send_players_the_phase(self.phase)
        deck = Deck()
        deck.populate_and_randomize()
        self.deal_cards(deck)
        ### deals with hand passing logic
        self.determine_passing()
        self.organize_hand()
    
    def determine_passing(self):
        if (len(self.rounds))%4 == 0:
            self.direction = 1
        elif (len(self.rounds))%4 == 1:
            self.direction = -1
        elif (len(self.rounds))%4 == 2:
            self.direction = 2
        else:
            self.direction = 0
        
    
    def get_player_with_channel(self, channel):
        for player in self.players:
            if player.channel.name == channel.name:
                return player

    def deal_cards(self, deck):
        '''Deal the cards to each player'''
        print ("Deck length", len(deck.cards))
        while len(deck.cards) > 0:
            for player in self.players:
                player.hand.append(deck.cards.pop())

    def send_players_their_cards(self):
        '''Sends a message to each player telling them which cards are 
        theirs'''
        for player in self.players:
            cards_str = ''
            for card in player.hand:
                cards_str += card.to_json()
            transmit(player.channel,{"Cards":cards_str})
            
    def send_player_valid_cards(self, channel, valid_cards):
        cards_str = ""
        for card in valid_cards:
                cards_str += card.to_json()
        transmit(channel,{"valid_cards":cards_str})
        
    def send_players_initial_valid_cards(self):
        for player in self.players:
            valid_cards = player.hand
            self.send_player_valid_cards(player.channel, valid_cards)
            
    def send_players_the_phase(self, phase):
        '''Sends a message to each player telling them which cards are 
        theirs'''
        for player in self.players:
            transmit(player.channel,{"game_phase": phase})
            
    def send_players_discard(self, player, discard):
        '''Sends a message to each player telling them which cards are 
        theirs'''
        discard_json = ""
        for card in discard:
            discard_json += card.to_json()
        transmit(self.group,{"discard": {"player": player.position, "card": discard_json}})
        
    def send_players_score(self):
        '''Sends a message to each player telling them the scores -- only
        updates after each hand'''
        score_list = []
        for player in self.players:
            score_list.append(str(player.game_points))
        transmit(self.group,{"scores": {"player": player.position, "score_list": score_list}})
        
    def organize_hand(self):
        for i in range(0,len(self.players)):
            self.players[i].hand.sort()
            print ("player %s's hand: %s" % (i ,self.players[i].hand))
        self.send_players_their_cards()
        self.send_players_initial_valid_cards()
        if self.direction != 0:
            self.pass_card_thing()
        else:
            self.phase = Game.IN_TRICK
            self.send_players_the_phase(self.phase)
            self.rounds[-1].phase = self.phase
            self.rounds[-1].tricks.append(TrickTurn(self.players, self.direction))
            next_player = self.who_goes_first()
            transmit(next_player.channel,{"your_turn": "true"})
        
    
    def tell_round_phase(self):
        self.rounds[-1].phase = self.phase
    
    def pass_cards_selected(self, cards_str, channel):
        cards = []
        for card_str in cards_str:
            cards.append(Card.from_short_string(card_str))
        player = self.get_player_with_channel(channel)
        everyone_passed = self.pass_round.passed_cards(player, cards)
        if everyone_passed:
            self.pass_round.set_hands_to_new_hands()
            self.send_players_their_cards()
            self.tell_round_phase()
            self.phase = Game.IN_TRICK
            self.send_players_the_phase(self.phase)
            self.rounds[-1].tricks.append(TrickTurn(self.players, self.direction, len(self.rounds[-1].tricks) == 0, self.hearts_broken))
            next_player = self.who_goes_first()
            #
            valid_cards = self.rounds[-1].tricks[-1].valid_cards_leader(next_player.hand)
            self.send_player_valid_cards(next_player.channel, valid_cards)
            #
            transmit(next_player.channel,{"your_turn": "true"})
      
    def trick_cards_selected(self, cards_str, channel):
        cards = []
        for card_str in cards_str:
            cards.append(Card.from_short_string(card_str))
        player = self.get_player_with_channel(channel)
        self.send_players_discard(player, cards)
        everyone_discarded = self.rounds[-1].tricks[-1].card_discarded(player, cards)
        if everyone_discarded:
            if self.hearts_broken == False:
                self.hearts_broken = self.rounds[-1].tricks[-1].are_hearts_broken()
            self.tricks_this_hand += 1
            next_player = self.rounds[-1].tricks[-1].get_winner()
            next_player.hand_points += self.rounds[-1].tricks[-1].get_trick_points()
            for player in self.players:
                player.hand = self.rounds[-1].tricks[-1].players_new_hands[player]
            self.send_players_their_cards()
            self.phase = Game.IN_TRICK
            self.tell_round_phase()
            self.send_players_the_phase(self.phase)
            self.rounds[-1].tricks.append(TrickTurn(self.players, self.direction, len(self.rounds[-1].tricks) == 0, self.hearts_broken))
            #
            valid_cards = self.rounds[-1].tricks[-1].valid_cards_leader(next_player.hand)
            self.send_player_valid_cards(next_player.channel, valid_cards)
            #
            transmit(next_player.channel,{"your_turn": "true"})
            ###################################################
            ##### BELOW IF STATEMENT IS THE END OF A HAND #####
            ###################################################
            if self.tricks_this_hand == self.trick_count: #normally 13 (set lower for test)
                self.tricks_this_hand = 0
                ####
                for i in self.players:
                    #checking if player shot the moon and if so applying exception#
                    if i.hand_points == 26:
                        for j in self.players:
                            j.hand_points = 27
                        i.hand_points = 0
                for i in self.players:
                    if i.hand_points == 27:
                        i.hand_points -= 1
                for i in self.players:
                    i.game_points += i.hand_points
                        ####
                for i in self.players:
                    i.hand_points = 0
                game_over = 0
                for i in self.players:
                    if i.game_points >= 100:
                        game_over += 1
                if game_over == 0:
                    self.send_players_score()
                    self.setup_game()
                else:
                    place_list = self.how_people_placed()
                    self.elo_calculation(place_list)
                    self.game_over()
        else:
            next_player = self.rounds[-1].tricks[-1].get_next_discarder()
            #
            valid_cards = self.rounds[-1].tricks[-1].valid_cards_follower(next_player.hand)
            self.send_player_valid_cards(next_player.channel, valid_cards)
            #
            transmit(next_player.channel,{"your_turn": "true"})
            
    def pass_card_thing(self):
        self.phase = Game.PASS_PHASE
        self.tell_round_phase()
        self.send_players_the_phase(self.phase)
        self.pass_round = PassRound(players=self.players, direction=self.direction)
            
    def who_goes_first(self):
        two_of_clubs = Card(2,'Clubs')
        for player in self.players:
            if two_of_clubs in player.hand:
                return player
            
    def how_people_placed(self):
        ''' gets scores for all players, sorts them, returns a list where
        the first element of the list is the position of the player who got first,
        the second element of the list is the position of the player who got second,
        etc. '''
        final_scores_list = []
        for i in range(0,len(self.players)):
            final_scores_list.append(int(str(self.players[i].game_points) + str(i)))
        final_scores_list.sort()
        place_list = []
        for i in range(0,len(self.players)):
            place_list.append(int(str(final_scores_list[i])[-1]))
        return place_list
    
    def game_over(self):
        pass
    
    def rank_calculation(self, place_list):
        
        placings = place_list
        
        ################################
        #Rank Points Section
        ################################
        
        player_rank = []
        
        for i in range(0,len(self.players)):
            player_rank.append(self.players[i].accounts.rank) # -3 new moon iv, -2 new moon iii,
        # -1 new moon ii, 0 new moon i, (main lobby)
        ##
        ## 1 waxing crescent I, 2 waxing crescent II, 3 waxing crescent III
        ##
        ## 4 half moon IV, 5 half moon V, 6 half moon VI
        ##
        ## 7 waxing gibbous VII, 8 waxing gibbous VIII, 9 waxing gibbous IX,
        ##
        ## 10 full moon X, 11 full moon XI, 12 full moon XII, 13 full moon XIII
        ##
        ## 14 harvest moon XIV, 15 harvest moon XV, 16 harvest moon XVI,
        ## 17 harvest moon XVII, 18 harvest moon XVIII
        ##
        ## 19 blue moon XIX, 20 blue moon XX
        
        #######
        #player rank progress list of stuff
        ######
        # if a player above 1st Dan) falls below zero rank progress they are demoted, ie -25/400  rank progress
        #getting set to the x/2x default
        # for the rank they are demoted to.
        # if a player hits the ceiling, they are promoted, set to the x/2x default, blah blah blah
        # 1 -- 200/400
        # 2 -- 400/800
        # 3 -- 600/1200
        # 4 -- 800/1600
        # 5 -- 1000/2000
        # 6 -- 1200/2400
        # 7 -- 1400/2800
        # etc...
        
        # the equation is defaults = rank x 200 (out of) rank x 400
        
        player_rank_progress = []
        
        for i in range(0,len(self.players)):
            player_rank_progress.append(self.players[i].accounts.rank_points)
        
        #rank_floor = less than zero
        
        which_lobby = 0 #TODO: CHANGE THIS LATER #### 0 = main lobby (new moon), 1 = waxing crescent
        # 2 = half moon, 3 = waxing gibbous, 4 = full moon, 5 = harvest moon, 6 = blue moon
        
        first_place_reward = [45,60,75,90,120,160,210] #lobby respective
        
        second_place_reward = [0,15,30,45,60,80,105] #dhgdshgkhsdjg
        
        third_place_reward = [0,0,0,0,0,0,0,0] #nothing for now, but it is here because maybe we
        # wanna change that later or for some lobby idk
        
        rank_based_fourth_punishments = [0,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330, 0, 0, 0]
        # for -3 through 20
        
        reward = []
        
        reward.append(first_place_reward[which_lobby])
        reward.append(second_place_reward[which_lobby])
        reward.append(third_place_reward[which_lobby])
        reward.append(rank_based_fourth_punishments[player_rank[3]])
        
        player_rank_progress_changed = []
        
        for i in range(0, len(self.players)):
            player_rank_progress_changed.append(player_rank_progress[i] + reward[i])
        
        for i in range(0, len(self.players)):
            if player_rank[i] < 0:
                if player_rank_progress_changed[i] == 0:
                    player_rank_progress[i] = 0
                else:
                    player_rank_progress[i] = 0
                    player_rank[i] += 1
            elif player_rank[i] == 0:
                if player_rank_progress_changed[i] == 0:
                    player_rank_progress[i] = 0
                else:
                    player_rank_progress[i] = 200
                    player_rank[i] += 1
            elif player_rank_progress_changed[i] < 0:
                if player_rank[i] == 1:
                    player_rank_progress[i] = 0
                else:
                    player_rank[i] -= 1
                    player_rank_progress[i] = 200*player_rank[i]
            elif player_rank_progress_changed[i] >= (player_rank[i]*400):
                player_rank[i] += 1
                player_rank_progress[i] = 200*player_rank[i]
            else:
                player_rank_progress[i] = player_rank_progress_changed[i]
        
        for i in range(0,len(self.players)):
            self.players[placings[i]].new_rank = player_rank[i]
            self.players[placings[i]].new_rank_progress = player_rank_progress[i]
      
    def elo_calculation(self, place_list):
        
        placings = place_list
        
        #games_played, #get the number of games that player has played, and this
        #should be set to one after their first game cus u don't wanna divide by 0
        #in my below equation lol#
        
        '''player_elo, #get this -- but ya default is 1500
        #print (player_elo)'''
        
        player_elo = []
        games_played = []
        average_other_elo = []
        elsa = 0
        divisor = []
        difference = []
        multiplier = [3,1,1,3]
        win_vs_other_player = [1,1,0,0]
        shifter = []
        elo_change = 0
        elo_change_final = []

        for i in range(0,len(self.players)):
            player_elo.append(self.players[placings[i]].accounts.elo)
            games_played.append(self.players[placings[i]].accounts.games_played)
            
        for i in range(0,len(self.players)):
            elsa = (float((player_elo[(i+1)%4] + player_elo[(i+2)%4] + player_elo[(i+3)%4]))/3)
            average_other_elo.append(elsa)
        
        for i in range(0,len(self.players)):
            difference.append(player_elo[i] - average_other_elo[i])
        
        # the more games played, the less elo change
        for i in range(0,len(self.players)):
            if games_played[i] >= 200:
                divisor.append(3)
            elif games_played[i] == 0:
                divisor.append(1)
            else:
                divisor.append(1 + (float(games_played[i])/100))
        
        #dealing with how much better/worse the player is
        for i in range(0,len(self.players)):
            shifter.append(1 + (float(abs(difference[i]))/1000))
        

        for i in range(0,len(self.players)):
            if difference[i] == 0:
                if win_vs_other_player[i] == 1:
                    elo_change = 10
                else:
                    elo_change = -10       
            elif difference[i] >= 500:
                if win_vs_other_player[i] == 1:
                    elo_change = 5
                else:
                    elo_change = -15
            elif difference[i] <= -500:
                if win_vs_other_player[i] == 1:
                    elo_change = 15
                else:
                    elo_change = -5
            else:
                if difference[i] < 0:
                    if win_vs_other_player[i] == 1:
                        elo_change = float(10)*shifter[i]
                    else:
                        elo_change = -(float(10)/shifter[i])
                else:
                    if win_vs_other_player[i] == 1:
                        elo_change = float(10)/shifter[i]
                    else:
                        elo_change = -(float(10)*shifter[i])
            elo_change = (float(elo_change)/divisor[i]) * multiplier[i]
            elo_change = round(elo_change, 1)
            elo_change_final.append(elo_change)
            
        for i in range(0,len(self.players)):
            self.players[placings[i]].new_elo = self.players[placings[i]].accounts.elo + elo_change_final[i]
            
            
            
            
            
                