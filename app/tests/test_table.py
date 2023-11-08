from django.test import TestCase
from .factories import TeamModelFactory, GameModelFactory
from app.utils.table import TableCounter


class DifferentTotalPointsTest(TestCase):
    """
     Pos. │ Team  │ Total Points
    ──────┼───────┼──────────────
      1   │ Team1 │      12
      2   │ Team0 │      6
      3   │ Team2 │      0
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(3)
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="3-6")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="3-0")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="3-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="0-1")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="2-1")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="0-1")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[1].name]["total_points"], 12)
        self.assertEqual(self.table[1][self.teams[0].name]["total_points"], 6)
        self.assertEqual(self.table[2][self.teams[2].name]["total_points"], 0)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[1].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[0].name]["position"], 2)
        self.assertEqual(self.table[2][self.teams[2].name]["position"], 3)


class SameTotalPointsTest(TestCase):
    """
     Pos. │ Team  │ Total Points │ Direct Points
    ──────┼───────┼──────────────┼───────────────
      1   │ Team1 │      7       │       4
      2   │ Team0 │      7       │       1
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(3)
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="0-2")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="1-1")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="3-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="1-0")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="2-1")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="0-1")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[1].name]["total_points"], 7)
        self.assertEqual(self.table[1][self.teams[0].name]["total_points"], 7)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[1].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[0].name]["position"], 2)


class SameDirectPointsTest(TestCase):
    """
     Pos. │ Team  │ Total Points │ Direct Points │ Direct Goal Difference
    ──────┼───────┼──────────────┼───────────────┼────────────────────────
      1   │ Team2 │      5       │       3       │           1
      2   │ Team0 │      5       │       3       │           -1
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(3)
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="1-1")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="1-1")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="1-1")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="1-1")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="0-2")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="0-1")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[2].name]["total_points"], 5)
        self.assertEqual(self.table[1][self.teams[0].name]["total_points"], 5)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[2].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[0].name]["position"], 2)


class SameDirectGoalDifferenceTest(TestCase):
    """
     Pos. │ Team  │ TP │ DP │ DGD │ Total Goal Difference
    ──────┼───────┼────┼────┼─────┼───────────────────────
      1   │ Team0 │ 9  │ 3  │  0  │           5
      2   │ Team1 │ 9  │ 3  │  0  │           2
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(3)
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="1-2")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="1-2")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="2-1")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="1-2")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="2-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="0-3")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[0].name]["total_points"], 9)
        self.assertEqual(self.table[1][self.teams[1].name]["total_points"], 9)

        self.assertEqual(self.table[0][self.teams[0].name]["goal_difference"], 5)
        self.assertEqual(self.table[1][self.teams[1].name]["goal_difference"], 2)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[0].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[1].name]["position"], 2)


class SameTotalGoalDifferenceTest(TestCase):
    """
     Pos. │ Team  │ TP │ DP │ DGD │ TGD │ Total Goals
    ──────┼───────┼────┼────┼─────┼─────┼─────────────
      1   │ Team2 │ 9  │ 3  │  0  │  2  │      9
      2   │ Team0 │ 9  │ 3  │  0  │  2  │      7
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(3)
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="2-1")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="1-2")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="2-3")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="3-2")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="0-3")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="0-3")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[2].name]["total_points"], 9)
        self.assertEqual(self.table[1][self.teams[0].name]["total_points"], 9)

        self.assertEqual(self.table[0][self.teams[2].name]["goal_difference"], 2)
        self.assertEqual(self.table[1][self.teams[0].name]["goal_difference"], 2)

        self.assertEqual(self.table[0][self.teams[2].name]["total_goals"], 9)
        self.assertEqual(self.table[1][self.teams[0].name]["total_goals"], 7)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[2].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[0].name]["position"], 2)


class SameTotalGoalsAndWinsTest(TestCase):
    """
     Pos. │ Team  │ TP │ DP │ DGD │ TGD │ TG │ Wins │ Wins Away
    ──────┼───────┼────┼────┼─────┼─────┼────┼──────┼───────────
      1   │ Team2 │ 7  │ 3  │  0  │  1  │ 7  │  2   │     2
      2   │ Team0 │ 7  │ 3  │  0  │  1  │ 7  │  2   │     1
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(3)
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="2-1")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="2-2")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="1-2")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="2-2")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="0-3")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="0-3")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[2].name]["total_points"], 7)
        self.assertEqual(self.table[1][self.teams[0].name]["total_points"], 7)

        self.assertEqual(self.table[0][self.teams[2].name]["goal_difference"], 1)
        self.assertEqual(self.table[1][self.teams[0].name]["goal_difference"], 1)

        self.assertEqual(self.table[0][self.teams[2].name]["total_goals"], 7)
        self.assertEqual(self.table[1][self.teams[0].name]["total_goals"], 7)

        self.assertEqual(self.table[0][self.teams[2].name]["total_wins"], 2)
        self.assertEqual(self.table[1][self.teams[0].name]["total_wins"], 2)

        self.assertEqual(self.table[0][self.teams[2].name]["wins_away"], 2)
        self.assertEqual(self.table[1][self.teams[0].name]["wins_away"], 1)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[2].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[0].name]["position"], 2)


class CombinedTableOneTest(TestCase):
    """
     Pos. │ Team  │ TP │ DP │ DP │ DGD
    ──────┼───────┼────┼────┼────┼─────
      1   │ Team3 │ 8  │ 8  │    │
      2   │ Team2 │ 8  │ 4  │ 3  │  1
      2   │ Team1 │ 8  │ 4  │ 3  │  -1
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(4)
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="2-1")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="2-0")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[3], result="2-2")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[1], result="2-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[3], result="0-3")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[2], result="2-2")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="9-0")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="0-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="2-0")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="0-0")
        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[3].name]["total_points"], 8)
        self.assertEqual(self.table[1][self.teams[2].name]["total_points"], 8)
        self.assertEqual(self.table[2][self.teams[1].name]["total_points"], 8)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[3].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[2].name]["position"], 2)
        self.assertEqual(self.table[2][self.teams[1].name]["position"], 3)


class CombinedTableTwoTest(TestCase):
    """
     Pos. │ Team  │ TP │ DP │ DGD │ TGD
    ──────┼───────┼────┼────┼─────┼─────
      1   │ Team4 │ 12 │ 12 │     │
      2   │ Team3 │ 12 │ 7  │  4  │
      3   │ Team2 │ 12 │ 7  │ -2  │  2
      4   │ Team1 │ 12 │ 7  │ -2  │ -2
    """
    def setUp(self):
        self.teams = TeamModelFactory.create_batch(6)
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[2], result="2-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[1], result="2-0")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[3], result="1-0")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[1], result="3-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[3], result="0-3")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[2], result="0-1")
        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[4], result="0-0")
        GameModelFactory.create(team_home=self.teams[4], team_away=self.teams[1], result="1-0")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[4], result="0-0")
        GameModelFactory.create(team_home=self.teams[4], team_away=self.teams[2], result="1-0")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[4], result="0-0")
        GameModelFactory.create(team_home=self.teams[4], team_away=self.teams[3], result="1-0")

        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[0], result="2-1")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[1], result="2-2")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[0], result="6-1")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[2], result="2-2")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[0], result="2-1")
        GameModelFactory.create(team_home=self.teams[0], team_away=self.teams[3], result="2-2")

        GameModelFactory.create(team_home=self.teams[1], team_away=self.teams[5], result="2-2")
        GameModelFactory.create(team_home=self.teams[2], team_away=self.teams[5], result="2-2")
        GameModelFactory.create(team_home=self.teams[3], team_away=self.teams[5], result="2-2")

        self.table = TableCounter().tableJSON()

    def test_stats(self):
        self.assertEqual(self.table[0][self.teams[4].name]["total_points"], 12)
        self.assertEqual(self.table[1][self.teams[3].name]["total_points"], 12)
        self.assertEqual(self.table[2][self.teams[2].name]["total_points"], 12)
        self.assertEqual(self.table[3][self.teams[1].name]["total_points"], 12)

        self.assertEqual(self.table[2][self.teams[2].name]["goal_difference"], 2)
        self.assertEqual(self.table[3][self.teams[1].name]["goal_difference"], -2)

    def test_positions(self):
        self.assertEqual(self.table[0][self.teams[4].name]["position"], 1)
        self.assertEqual(self.table[1][self.teams[3].name]["position"], 2)
        self.assertEqual(self.table[2][self.teams[2].name]["position"], 3)
        self.assertEqual(self.table[3][self.teams[1].name]["position"], 4)
