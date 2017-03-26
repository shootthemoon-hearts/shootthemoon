from django.test import TestCase
from unittest.mock import MagicMock
from game_app.player import Player
from game_app.game import Game
from game_app.accounts import Account

class GameTestCase(TestCase):
    def setUp(self):
        self.players = []
        for _ in range(0,4):
            player = Player(MagicMock())
            self.players.append(player)
            player.accounts = Account()
        
        self.game = Game(MagicMock(),3)
        self.game.players = self.players

    def test_how_people_placed(self):
        self.players[0].game_points = 130
        self.players[1].game_points = 120
        self.players[2].game_points = 121
        self.players[3].game_points = 13
        
        listExpected = self.game.how_people_placed()
        listActual = [3,1,2,0]
        
        self.assertListEqual(listExpected, listActual)
        
        storeExpected = self.players[3].place_this_game
        storeActual = 0
        
        self.assertEqual(storeExpected, storeActual)
        
    def test_how_people_placed_tie(self):
        self.players[0].game_points = 130
        self.players[1].game_points = 13
        self.players[2].game_points = 121
        self.players[3].game_points = 13
        
        listExpected = self.game.how_people_placed()
        listActual = [1,3,2,0]
        
        self.assertListEqual(listExpected, listActual)
        
    def test_elo_calculation(self):
        place_list = [3,0,1,2]
        for i in range(0,4):
            self.game.players[i].accounts.elo = 1500
            self.game.players[i].accounts.games_played = 0
        
        self.game.elo_calculation(place_list)
        
        eloExpected = self.players[3].new_elo
        eloActual = 1530
        
        self.assertEqual(eloExpected, eloActual)
        
    def test_rank_calculation(self):
        place_list = [1,3,2,0]
        for i in range(0,4):
            self.game.players[i].accounts.rank = 1
            self.game.players[i].accounts.rank_points = 200
            
        self.game.rank_calculation(place_list)
        
        rankExpected = self.players[1].new_rank
        rankActual = 1
        
        self.assertEqual(rankExpected, rankActual)
        
        rankProgressExpected = self.players[1].new_rank_progress
        rankProgressActual = 245
        
        self.assertEqual(rankProgressExpected, rankProgressActual)
        
        