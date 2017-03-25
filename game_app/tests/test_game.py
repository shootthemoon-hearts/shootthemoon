from django.test import TestCase
from unittest.mock import MagicMock
from game_app.player import Player
from game_app.game import Game

class GameTestCase(TestCase):
    def setUp(self):
        self.players = []
        for _ in range(0,4):
            self.players.append(Player(MagicMock()))
        
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
        
    def test_how_people_placed_tie(self):
        self.players[0].game_points = 130
        self.players[1].game_points = 13
        self.players[2].game_points = 121
        self.players[3].game_points = 13
        
        listExpected = self.game.how_people_placed()
        listActual = [1,3,2,0]
        
        self.assertListEqual(listExpected, listActual)
        
        
        
        