from game_app.models.account import Account
from game_app.models.game import Game
from django.db import transaction


def rank_calculation(game, place_list):
    
    placings = place_list
    
    ################################
    #Rank Points Section
    ################################
    
    player_rank = []
    
    for i in range(0,len(game.player_set.all())):
        player_rank.append(game.player_set.all()[i].accounts.rank) # -3 new moon iv, -2 new moon iii,
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
    
    for i in range(0,len(game.player_set.all())):
        player_rank_progress.append(game.player_set.all()[i].accounts.rank_points)
    
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
    
    for i in range(0, len(game.player_set.all())):
        player_rank_progress_changed.append(player_rank_progress[i] + reward[i])
    
    for i in range(0, len(game.player_set.all())):
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
    
    for i in range(0,len(game.player_set.all())):
        game.player_set.all()[placings[i]].new_rank = player_rank[i]
        game.player_set.all()[placings[i]].new_rank_progress = player_rank_progress[i]
        game.player_set.all()[placings[i]].save()
  
def elo_calculation(game):
    
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
    accounts = []
    
    player_list = [player for player in game.player_set.all()]
    player_list.sort(key=lambda player: player.place_this_game)

    with transaction.atomic():
        for player in player_list:
            # Assume only one account
            account = Account.objects.select_for_update().filter(user__id = player.user.id).get()
            player_elo.append(account.elo)
            accounts.append(account)
            
        for i in range(0,len(player_list)):
            elsa = (float((player_elo[(i+1)%4] + player_elo[(i+2)%4] + player_elo[(i+3)%4]))/3)
            average_other_elo.append(elsa)
        
        for i in range(0,len(player_list)):
            difference.append(player_elo[i] - average_other_elo[i])
        
        # the more games played, the less elo change
        for player in player_list:
            games_played = Game.objects.filter(player__user=player.user, active=False).distinct().count()
            if games_played >= 200:
                divisor.append(3)
            elif games_played == 0:
                divisor.append(1)
            else:
                divisor.append(1 + (float(games_played)/100))
        
        #dealing with how much better/worse the player is
        for i in range(0,len(player_list)):
            shifter.append(1 + (float(abs(difference[i]))/1000))
        

        for i in range(0,len(player_list)):
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

        for i in range(0, len(player_list)):
            accounts[i].elo = player_elo[i] + elo_change_final[i]
            accounts[i].save()
        