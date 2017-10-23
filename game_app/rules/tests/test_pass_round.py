import mock

from django.test import TestCase

from game_app.card import Card
from game_app.models import GameRound
from game_app.models import PassRound
from game_app.models import Player

from game_app.rules.pass_direction import PASS_DIRECTION
from game_app.rules import pass_round


class Test(TestCase):
    def setUp(self):
        self.pr = PassRound.objects.create(id=1,
                                           game_round=GameRound.objects.create(),
                                           active=False,
                                           direction=PASS_DIRECTION.LEFT,
                                           passed_cards=[],
                                           seats_received=[0])
        self.player = Player.objects.create(id=2, disconnected=False,
                                            enrolled_queue=None,
                                            enrolled_game=None,
                                            channel='', position=0, hand=[],
                                            game_points=0,
                                            hand_points=0, bank_ms=10000,
                                            user=None,
                                            time_turn_started=None,
                                            new_elo=0, place_this_game=0)

    @mock.patch('game_app.rules.pass_round.has_everyone_passed')
    def test_received_passed_cards_first_pass_valid(self, has_everyone_passed):
        pr = self.pr
        pr.id = 1
        pr.active = True
        pr.seats_received = []
        pr.passed_cards = []
        pr.save()

        pass_cards = (
            [Card(2, Card.CLUBS), Card(3, Card.CLUBS), Card(4, Card.CLUBS)])

        player = self.player
        player.id = 2
        player.position = 0
        player.hand = pass_cards
        player.save()

        has_everyone_passed.return_value = False

        pass_round.received_passed_cards(pass_cards, 2, 1)

        pr.refresh_from_db()

        self.assertListEqual(pass_cards, pr.passed_cards)
        self.assertListEqual([0], pr.seats_received)

    @mock.patch('game_app.rules.pass_round.has_everyone_passed')
    def test_received_passed_cards_middle_pass_valid(self, has_everyone_passed):
        pr = self.pr
        pr.id = 1
        pr.active = True
        pr.seats_received = [0, 2]
        pr.passed_cards = [Card(2, Card.CLUBS), Card(3, Card.CLUBS),
                           Card(4, Card.CLUBS), Card(8, Card.CLUBS),
                           Card(9, Card.CLUBS), Card(10, Card.CLUBS)]
        pr.save()

        pass_cards = (
            [Card(5, Card.CLUBS), Card(6, Card.CLUBS), Card(7, Card.CLUBS)])

        player = self.player
        player.id = 2
        player.position = 1
        player.hand = pass_cards
        player.save()

        has_everyone_passed.return_value = False


        pass_round.received_passed_cards(pass_cards, 2, 1)

        pr.refresh_from_db()

        expected_cards = [Card(2, Card.CLUBS), Card(3, Card.CLUBS),
                          Card(4, Card.CLUBS), Card(5, Card.CLUBS),
                          Card(6, Card.CLUBS), Card(7, Card.CLUBS),
                          Card(8, Card.CLUBS), Card(9, Card.CLUBS),
                          Card(10, Card.CLUBS)]
        self.assertListEqual(expected_cards, pr.passed_cards)
        self.assertListEqual([0, 1, 2], pr.seats_received)

    def test_received_passed_cards_pass_round_inactive_invalid(self):
        pr = self.pr
        pr.id = 1
        pr.active = False
        pr.seats_received = []
        pr.passed_cards = []
        pr.save()

        pass_cards = (
            [Card(5, Card.CLUBS), Card(6, Card.CLUBS), Card(7, Card.CLUBS)])

        player = self.player
        player.id = 2
        player.position = 1
        player.hand = pass_cards
        player.save()

        pass_round.received_passed_cards(pass_cards, 2, 1)

        pr.refresh_from_db()

        expected_cards = []
        self.assertListEqual(expected_cards, pr.passed_cards)
        self.assertListEqual([], pr.seats_received)

    def test_received_passed_cards_pass_round_wrong_card_amount_invalid(self):
        pr = self.pr
        pr.id = 1
        pr.active = True
        pr.seats_received = []
        pr.passed_cards = []
        pr.save()

        pass_cards = (
            [Card(5, Card.CLUBS), Card(6, Card.CLUBS), Card(7, Card.CLUBS)])

        player = self.player
        player.id = 2
        player.position = 1
        player.save()

        pass_cards = [Card(5, Card.CLUBS)]

        pass_round.received_passed_cards(pass_cards, 2, 1)

        pr.refresh_from_db()

        expected_cards = []
        self.assertListEqual(expected_cards, pr.passed_cards)
        self.assertListEqual([], pr.seats_received)

    def test_received_passed_cards_pass_round_card_not_in_hand_invalid(self):
        pr = self.pr
        pr.id = 1
        pr.active = True
        pr.seats_received = []
        pr.passed_cards = []
        pr.save()

        pass_cards = (
            [Card(5, Card.CLUBS), Card(6, Card.CLUBS), Card(7, Card.CLUBS)])

        player = self.player
        player.id = 2
        player.position = 1
        player.save()

        pass_cards = (
            [Card(4, Card.CLUBS), Card(6, Card.CLUBS), Card(7, Card.CLUBS)])

        pass_round.received_passed_cards(pass_cards, 2, 1)

        pr.refresh_from_db()

        expected_cards = []
        self.assertListEqual(expected_cards, pr.passed_cards)
        self.assertListEqual([], pr.seats_received)
