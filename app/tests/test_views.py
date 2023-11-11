from django.test import TestCase, Client
from django.urls import reverse
from .factories import TeamModelFactory


class TestViewIndex(TestCase):
    def setUp(self):
        TeamModelFactory.create_batch(3)
        self.client = Client()

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/home.html')

    def test_view_context_processor_teams_amount(self):
        response = self.client.get(reverse('index'))
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
