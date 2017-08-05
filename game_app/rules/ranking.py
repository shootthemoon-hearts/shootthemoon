from game_app.models.account import Account
from game_app.models.game import Game
from django.db import transaction
from stats.rank_constants import Rank

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
            #rank
            if accounts[i].rank == Rank.newMoon:
                if accounts[i].elo >= 1700:
                    accounts[i].rank = Rank.waxingCrescent
            elif accounts[i].rank == Rank.waxingCrescent:
                if accounts[i].elo < 1650:
                    accounts[i].rank = Rank.newMoon
                elif accounts[i].elo >= 1900:
                    accounts[i].rank = Rank.firstQuarter
            elif accounts[i].rank == Rank.firstQuarter:
                if accounts[i].elo < 1850:
                    accounts[i].rank = Rank.waningCrescent
                elif accounts[i].elo >= 2100:
                    accounts[i].rank = Rank.waxingGibbous
            elif accounts[i].rank == Rank.waxingGibbous:
                if accounts[i].elo < 2050:
                    accounts[i].rank = Rank.lastQuarter
                elif accounts[i].elo >= 2300:
                    accounts[i].rank = Rank.fullMoon
            elif accounts[i].rank == Rank.fullMoon:
                if accounts[i].elo < 2250:
                    accounts[i].rank = Rank.waningGibbous
                elif accounts[i].elo >= 2500:
                    accounts[i].rank = Rank.blueMoon
            elif accounts[i].rank == Rank.blueMoon:
                if accounts[i].elo < 2450:
                    accounts[i].rank = Rank.lightBlueMoon
            #/rank
            accounts[i].save()
        