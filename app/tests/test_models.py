from django.test import TestCase

from .factories import TeamModelFactory, PlayerModelFactory, GameModelFactory, GoalModelFactory
from datetime import date
from random import randint


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = TeamModelFactory()

    def test_team_creation(self):
        self.team.save()
        self.assertIsNotNone(self.team.id)
        self.assertEqual(self.team.name, self.team.__str__())

    def test_team_finished_games(self):
        GameModelFactory.create_batch(3, team_away=self.team)
        GameModelFactory.create_batch(2, team_home=self.team)
        GameModelFactory(team_home=self.team, result="None-None")
        self.assertEqual(self.team.finished_games().count(), 5)

    def test_team_squad(self):
        PlayerModelFactory.create_batch(11, team=self.team)
        self.assertEqual(self.team.squad.count(), 11)

    def test_get_all_imported_id(self):
        list_of_ids = ["AF#999", "vtXde3AAA", "AF#GG55", "24452"]

        for imported_id in list_of_ids:
            TeamModelFactory.create(imported_from=imported_id)

        self.assertEqual(set(list_of_ids), set(self.team.get_all_imported_id()))


class PlayerModelTest(TestCase):
    def setUp(self):
        self.player = PlayerModelFactory()

    def test_player_creation(self):
        self.player.save()
        self.assertIsNotNone(self.player.id)
        self.assertEqual(self.player.full_name, self.player.__str__())

    def test_player_age(self):
        random_age = randint(16, 40)
        player_for_test_age = PlayerModelFactory.create(
            birth_date=date.today().replace(year=date.today().year - random_age)
        )
        self.assertEqual(type(self.player.age), int)
        self.assertEqual(player_for_test_age.age, random_age)

    def test_player_own_goals(self):
        GoalModelFactory.create_batch(2, scorer=None, own_goal=True, own_goal_scorer=self.player)
        GoalModelFactory.create_batch(5, scorer=self.player)
        self.assertEqual(self.player.player_own_goals.count(), 2)


class GameModelTest(TestCase):
    def setUp(self):
        self.game = GameModelFactory()

    def test_game_creation(self):
        self.game.save()
        self.assertIsNotNone(self.game.id)
        self.assertEqual(f"{self.game.team_home} {self.game.result} {self.game.team_away}", self.game.__str__())

    def test_game_goals(self):
        GoalModelFactory.create_batch(3, game=self.game)
        self.assertEqual(self.game.game_goals.count(), 3)


class GoalModelTest(TestCase):
    def setUp(self):
        self.goal = GoalModelFactory()

    def test_goal_creation(self):
        self.goal.save()
        self.assertIsNotNone(self.goal.id)
