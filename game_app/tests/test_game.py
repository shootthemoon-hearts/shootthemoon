from django.test import TestCase
from unittest.mock import MagicMock
from game_app.models.player import Player
from game_app.rules import game_round
from game_app.models.game import Game
from game_app.models.account import Account
from game_app.rules import ranking
from django.contrib.auth.models import User
from stats.rank_constants import Rank

class GameTestCase(TestCase):
#     def setUp(self):
#         self.players = []
#         for _ in range(0,4):
#             player = Player(MagicMock())
#           
        
#         self.game = game(MagicMock())
#         self.game.players = self.players

#     def test_how_people_placed(self):
#         self.players[0].game_points = 130
#         self.players[1].game_points = 120
#         self.players[2].game_points = 121
#         self.players[3].game_points = 13
#         
#         listExpected = self.game.save_how_people_placed()
#         listActual = [3,1,2,0]
#         
#         self.assertListEqual(listExpected, listActual)
#         
#         storeExpected = self.players[3].place_this_game
#         storeActual = 0
#         
#         self.assertEqual(storeExpected, storeActual)
#         
#     def test_how_people_placed_tie(self):
#         self.players[0].game_points = 130
#         self.players[1].game_points = 13
#         self.players[2].game_points = 121
#         self.players[3].game_points = 13
#         
#         listExpected = self.game.save_how_people_placed()
#         listActual = [1,3,2,0]
#         
#         self.assertListEqual(listExpected, listActual)
        
    def test_elo_calculation(self):
        
        self.game = Game()
        
        self.game.active = True
        
        self.game.save()
        
        self.players = []
        self.accounts = []
        for i in range(0,4):
            playa = Player()
            playa.new_elo = 0
            playa.place_this_game = i
            playa.user = User.objects.create_user(str(i),None,str(i))
            accoont = Account.objects.create()
            accoont.elo = 1650
            accoont.rank = "waxingCrescent"
            accoont.user = playa.user
            accoont.save()
            playa.id = i+1
            playa.save()
            #
            self.accounts.append(accoont)
            self.players.append(playa)
            self.players[i].enrolled_game = self.game
            self.players[i].save()
        
        for player in self.players:
            # Assume only one account
            account = Account.objects.select_for_update().filter(user__id = player.user.id).get()
            self.accounts.append(account)
            
        ranking.elo_calculation(self.game)
        
        self.accounts = []
        
        for player in self.players:
            # Assume only one account
            account = Account.objects.select_for_update().filter(user__id = player.user.id).get()
            self.accounts.append(account)
        
        #eloExpected for 1500all -- 1530,1510,1490,1470
        
        print("1st: ",self.accounts[0].elo)
        print("2nd: ",self.accounts[1].elo)
        print("3rd: ",self.accounts[2].elo)
        print("4th: ",self.accounts[3].elo)
        print("1strank: ",self.accounts[0].rank)
        print("2ndrank: ",self.accounts[1].rank)
        print("3rdrank: ",self.accounts[2].rank)
        print("4thrank: ",self.accounts[3].rank)
        
        #print(eloActual)
        #self.assertEqual(eloExpected, eloActual)
#     def test_rank_calculation(self):
#         place_list = [1,3,2,0]
#         for i in range(0,4):
#             self.game.players[i].accounts.rank = 1
#             self.game.players[i].accounts.rank_points = 200
#             
#         self.game.rank_calculation(place_list)
#         
#         rankExpected = self.players[1].new_rank
#         rankActual = 1
#         
#         self.assertEqual(rankExpected, rankActual)
#         
#         rankProgressExpected = self.players[1].new_rank_progress
#         rankProgressActual = 245
#         
#         self.assertEqual(rankProgressExpected, rankProgressActual)
        
        