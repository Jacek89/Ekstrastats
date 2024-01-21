from django.test import TestCase, Client
from django.urls import reverse
from .factories import TeamModelFactory, GameModelFactory, GoalModelFactory
from django.core.cache import cache


class TestViewIndex(TestCase):
    def setUp(self):
        TeamModelFactory.create_batch(3)
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/home.html')

    def test_view_context_processor_teams_amount(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['teams_extra']), 3)


class TestViewTable(TestCase):
    def setUp(self):
        TeamModelFactory.create_batch(18)
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('table'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('table'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/table.html')

    def test_view_table_ajax_response(self):
        response = self.client.get(reverse('table'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_view_table_teams_amount(self):
        response = self.client.get(reverse('table'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(response.json()["data"]), 18)

    def tearDown(self):
        cache.delete('table')


class TestViewTeam(TestCase):
    def setUp(self):
        self.team = TeamModelFactory.create()
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('team_main', args=(self.team.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('team_main', args=(self.team.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/team.html')

    def test_view_team_in_context(self):
        response = self.client.get(reverse('team_main', args=(self.team.id,)))
        self.assertContains(response, self.team.name)


class TestViewStatistics(TestCase):
    def setUp(self):
        GameModelFactory.create_batch(2)
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/statistics.html')


class TestViewTeamStats(TestCase):
    def setUp(self):
        cache.delete('table')
        self.teams = TeamModelFactory.create_batch(3)
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('team_stats', args=(self.teams[0].id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('team_stats', args=(self.teams[0].id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/team_stats.html')

    def test_view_team_in_context(self):
        response = self.client.get(reverse('team_stats', args=(self.teams[0].id,)))
        self.assertContains(response, self.teams[0].name)

    def tearDown(self):
        cache.delete('table')


class TestViewRoundSummary(TestCase):
    def setUp(self):
        games = GameModelFactory.create_batch(9, round=1)
        GoalModelFactory.create_batch(2, game=games[0])
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('round', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('round', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/round.html')

    def test_view_context_round_num(self):
        response = self.client.get(reverse('round', args=(1,)))
        self.assertEqual(response.context["round_num"], 1)

    def test_view_context_game_played(self):
        response = self.client.get(reverse('round', args=(1,)))
        self.assertEqual(response.context["num_games"], 9)

    def test_view_context_total_goals(self):
        response = self.client.get(reverse('round', args=(1,)))
        self.assertEqual(response.context["total_goals"], 2)

    def test_view_context_goals_per_game(self):
        response = self.client.get(reverse('round', args=(1,)))
        self.assertAlmostEqual(response.context["goals_per_game"], 0.22)
