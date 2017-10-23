import datetime
import mock
from mock import MagicMock
from django.test import TestCase
from django.utils import timezone

from game_app.models import GameRound
from game_app.models import TrickTurn
from game_app.models import Player
from game_app.rules import trick_turn as trick_turn_rules
from game_app.card import Card


class Test(TestCase):

    def setUp(self):
        self.tt = TrickTurn.objects.create(id=1, game_round=GameRound.objects.create(), active=False,
                                      number=0, first_seat=0,
                                      discards=[], expected_seat=0,
                                      hearts_broken=False)
        self.player = Player.objects.create(id=2, disconnected=False,
                                       enrolled_queue=None, enrolled_game=None,
                                       channel='', position=0, hand=[], game_points=0,
                                       hand_points=0, bank_ms=10000, user=None,
                                       time_turn_started=None,
                                       new_elo=0, place_this_game=0)


    @mock.patch('game_app.rules.trick_turn.send_players_discard')
    @mock.patch('game_app.rules.trick_turn.finish')
    @mock.patch('game_app.rules.trick_turn.send_turn_notification')
    def test_card_discarded_first_turn_valid(self, send_turn_notification, finish, send_players_discard):
        old_hand = [Card(2, Card.CLUBS)]
        time_turn_started = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 0, 0))
        time_turn_ended = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 7, 0))

        tt = self.tt
        tt.id = 1
        tt.active = True
        tt.discards = []
        tt.save()

        player = self.player
        player.id = 2
        player.position = 0
        player.hand = old_hand
        player.bank_ms = 10000
        player.time_turn_started = time_turn_started
        player.save()

        discard = Card(2, Card.CLUBS)
        trick_turn_rules.card_discarded(discard, 2, 1, time_turn_ended)

        tt.refresh_from_db()
        player.refresh_from_db()

        self.assertListEqual([discard], tt.discards)
        self.assertEqual(1, tt.expected_seat)

        self.assertListEqual([], player.hand)
        self.assertEqual(8000, player.bank_ms)

    @mock.patch('game_app.rules.trick_turn.send_players_discard')
    @mock.patch('game_app.rules.trick_turn.finish')
    @mock.patch('game_app.rules.trick_turn.send_turn_notification')
    def test_card_discarded_invalid_trick_id(self, send_turn_notification, finish, send_players_discard):
        old_hand = [Card(2, Card.CLUBS)]
        time_turn_started = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 0, 0))
        time_turn_ended = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 4, 0))

        tt = self.tt
        tt.id = 9
        tt.active = True
        tt.discards = []
        tt.save()

        player = self.player
        player.id = 2
        player.position = 0
        player.hand = old_hand
        player.bank_ms = 10000
        player.time_turn_started = time_turn_started
        player.save()

        discard = Card(2, Card.CLUBS)
        trick_turn_rules.card_discarded(discard, 2, 1, time_turn_ended)

        tt.refresh_from_db()
        player.refresh_from_db()

        self.assertListEqual([], tt.discards)
        self.assertEqual(0, tt.expected_seat)

        self.assertListEqual(old_hand, player.hand)
        self.assertEqual(10000, player.bank_ms)

    @mock.patch('game_app.rules.trick_turn.send_players_discard')
    @mock.patch('game_app.rules.trick_turn.finish')
    @mock.patch('game_app.rules.trick_turn.send_turn_notification')
    def test_card_discarded_trick_inactive(self, send_turn_notification, finish, send_players_discard):
        old_hand = [Card(2, Card.CLUBS)]
        time_turn_started = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 0, 0))
        time_turn_ended = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 4, 0))

        tt = self.tt
        tt.id = 1
        tt.active = False
        tt.discards = []
        tt.save()

        player = self.player
        player.id = 2
        player.position = 0
        player.hand = old_hand
        player.bank_ms = 10000
        player.time_turn_started = time_turn_started
        player.save()

        discard = Card(2, Card.CLUBS)
        trick_turn_rules.card_discarded(discard, 2, 1, time_turn_ended)

        tt.refresh_from_db()
        player.refresh_from_db()

        self.assertListEqual([], tt.discards)
        self.assertEqual(0, tt.expected_seat)

        self.assertListEqual(old_hand, player.hand)
        self.assertEqual(10000, player.bank_ms)

    @mock.patch('game_app.rules.trick_turn.send_players_discard')
    @mock.patch('game_app.rules.trick_turn.finish')
    @mock.patch('game_app.rules.trick_turn.send_turn_notification')
    def test_card_discarded_leader_invalid_card(self, send_turn_notification, finish, send_players_discard):
        old_hand = [Card(2, Card.CLUBS)]
        time_turn_started = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 0, 0))
        time_turn_ended = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 4, 0))

        tt = self.tt
        tt.id = 1
        tt.active = True
        tt.first_seat = 0
        tt.discards = []
        tt.expected_seat = 0
        tt.save()

        player = self.player
        player.id = 2
        player.position = 0
        player.hand = old_hand
        player.bank_ms = 10000
        player.time_turn_started = time_turn_started
        player.save()

        discard = Card(2, Card.DIAMONDS)
        trick_turn_rules.card_discarded(discard, 2, 1, time_turn_ended)

        tt.refresh_from_db()
        player.refresh_from_db()

        self.assertListEqual([], tt.discards)
        self.assertEqual(0, tt.expected_seat)

        self.assertListEqual(old_hand, player.hand)
        self.assertEqual(10000, player.bank_ms)

    @mock.patch('game_app.rules.trick_turn.send_players_discard')
    @mock.patch('game_app.rules.trick_turn.finish')
    @mock.patch('game_app.rules.trick_turn.send_turn_notification')
    def test_card_discarded_follower_invalid_card(self, send_turn_notification, finish, send_players_discard):
        time_turn_started = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 0, 0))
        time_turn_ended = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 4, 0))

        old_discards = [Card(2, Card.CLUBS)]
        tt = self.tt
        tt.id = 1
        tt.active = True
        tt.first_seat = 0
        tt.discards = old_discards
        tt.expected_seat = 1
        tt.save()

        old_hand = [Card(3, Card.CLUBS)]
        player = self.player
        player.id = 2
        player.position = 1
        player.hand = old_hand
        player.bank_ms = 10000
        player.time_turn_started = time_turn_started
        player.save()

        discard = Card(2, Card.DIAMONDS)
        trick_turn_rules.card_discarded(discard, 2, 1, time_turn_ended)

        tt.refresh_from_db()
        player.refresh_from_db()

        self.assertListEqual(old_discards, tt.discards)
        self.assertEqual(1, tt.expected_seat)

        self.assertListEqual(old_hand, player.hand)
        self.assertEqual(10000, player.bank_ms)

    @mock.patch('game_app.rules.trick_turn.send_players_discard')
    @mock.patch('game_app.rules.trick_turn.finish')
    @mock.patch('game_app.rules.trick_turn.send_turn_notification')
    def test_card_discarded_not_your_turn(self, send_turn_notification, finish, send_players_discard):
        time_turn_started = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 0, 0))
        time_turn_ended = timezone.make_aware(datetime.datetime(2017, 10, 1, 0, 0, 4, 0))

        old_discards = [Card(2, Card.CLUBS)]
        tt = self.tt
        tt.id = 1
        tt.active = True
        tt.first_seat = 1
        tt.discards = old_discards
        tt.expected_seat = 1
        tt.save()

        old_hand = [Card(3, Card.CLUBS)]
        player = self.player
        player.id = 2
        player.position = 2
        player.hand = old_hand
        player.bank_ms = 10000
        player.time_turn_started = time_turn_started
        player.save()

        discard = Card(2, Card.DIAMONDS)
        trick_turn_rules.card_discarded(discard, 2, 1, time_turn_ended)

        tt.refresh_from_db()
        player.refresh_from_db()

        self.assertListEqual(old_discards, tt.discards)
        self.assertEqual(1, tt.expected_seat)

        self.assertListEqual(old_hand, player.hand)
        self.assertEqual(10000, player.bank_ms)