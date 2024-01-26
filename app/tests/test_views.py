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
        self.games = GameModelFactory.create_batch(4)
        GoalModelFactory.create(game=self.games[0], minute=10)
        GoalModelFactory.create(game=self.games[0], minute=60)
        GoalModelFactory.create(game=self.games[2], minute=12)
        GoalModelFactory.create(game=self.games[3], minute=8)
        GoalModelFactory.create(game=self.games[3], minute=40)
        GoalModelFactory.create(game=self.games[3], minute=46)
        GoalModelFactory.create(game=self.games[3], minute=90, minute_extra=3)

        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/statistics.html')

    def test_view_context_goals_15(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.context['goals_15'][15], 3)
        self.assertEqual(response.context['goals_15'][30], 0)
        self.assertEqual(response.context['goals_15'][45], 1)
        self.assertEqual(response.context['goals_15'][60], 2)
        self.assertEqual(response.context['goals_15'][75], 0)
        self.assertEqual(response.context['goals_15'][90], 1)

    def test_view_context_goals_45(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.context['goals_45'][45], 4)
        self.assertEqual(response.context['goals_45'][90], 3)

    def test_view_context_goals_per_game(self):
        response = self.client.get(reverse('statistics'))
        self.assertAlmostEqual(response.context['goals_per_game'], 1.75)

    def test_view_context_goals_sum(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.context['goals_sum'], 7)


class TestViewTeamStats(TestCase):
    def setUp(self):
        cache.delete('table')
        self.teams = TeamModelFactory.create_batch(3)
        self.games = GameModelFactory.create_batch(2, team_home=self.teams[0])
        self.games += GameModelFactory.create_batch(3, team_away=self.teams[0])
        GoalModelFactory.create_batch(3, team_against=self.teams[0], game=self.games[0])
        GoalModelFactory.create_batch(4, team_scored=self.teams[0], game=self.games[2])
        GoalModelFactory.create_batch(2, team_against=self.teams[0], game=self.games[2])
        GoalModelFactory.create_batch(3, team_scored=self.teams[0], game=self.games[3])
        GoalModelFactory.create_batch(5, team_scored=self.teams[0], game=self.games[4])

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

    def test_view_context_clean_sheets(self):
        response = self.client.get(reverse('team_stats', args=(self.teams[0].id,)))
        self.assertEqual(response.context['clean_sheets'], 3)

    def test_view_context_failed_to_score(self):
        response = self.client.get(reverse('team_stats', args=(self.teams[0].id,)))
        self.assertEqual(response.context['failed_to_score'], 2)

    def test_view_context_over25(self):
        response = self.client.get(reverse('team_stats', args=(self.teams[0].id,)))
        self.assertEqual(response.context['over25'], 4)

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
