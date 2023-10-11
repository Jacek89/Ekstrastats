from datetime import date
from app.models import Game, Team
from django.db.models import Q
from collections import defaultdict

TEAMS_IN_TABLE = 18

class TableCounter:
    """
    Class that counts Ekstraklasa table on init.

    If no arguments passed the all season table is the default.
    Can also return a table including only matches in a given time period.

    Attributes:
    date_from -- (str)(format: YYYY-MM-DD): Date from which matches are included.
    date_to -- (str)(format: YYYY-MM-DD): Date by which matches are included.

    Methods:
    tableJSON -- returns the Ekstraklasa table for the specified or the default period in JSON format
    """
    def __init__(self, date_from=None, date_to=None):
        if date_from is not None:
            self.date_from = date_from
        else:
            date_from = "2023-07-01"
        if date_to is not None:
            self.date_to = date_to
        else:
            date_to = date.today().strftime("%Y-%m-%d")

        self.date_from = date_from
        self.date_to = date_to
        self.games = Game.objects.filter(Q(date__range=[self.date_from, self.date_to]) & ~Q(result="None-None"))
        self.table = {}
        self.__count_table()

    @staticmethod
    def __add_stats(table: dict, team_name: str, **kwargs):
        """
        Method that adds stats (points, goals, games etc.) to team. Can add all stats to one team per call.

        Keywords Arguments:
        table -- dictionary representing a table. Empty dictionary can be passed.
        team_name -- the name of the team to which the stats will be added. If the team name is not in the table,
                     the function will add this team automatically and create a statistics template for this team.
        **kwargs -- statistics to be added: e.g. goals_away=2 will add two away goals to the team.
                    Statistics can be added: {"wins", "loses", "draws", "points", "goals", "goals_lost"}_{home", "away"}

        Returns:
        Dictionary representing of table, in the same form after adding the statistics.
        """
        try:
            table[team_name]
        except KeyError:
            stats = ["wins", "loses", "draws", "points", "goals", "goals_lost", "matches"]
            keys = ["home", "away"]
            table[team_name] = {
                f"{s}_{k}": 0 for s in stats for k in keys
            }
        for key, value in kwargs.items():
            try:
                table[team_name][key] += int(value)
            except KeyError:
                raise KeyError(
                    f'"{key}" not found in keyword list. You should use on of:'
                    '{"wins", "loses", "draws", "points", "goals", "goals_lost"}_{home", "away"}, e.g. "goals_away"')
            except ValueError:
                raise ValueError(f"'{value}' is not a number.")

        return table

    def __count_stats(self, games, table):
        """
        Method that extracts stats from games.

        Keywords Arguments:
        games -- Queryset of "Game" models.
        table -- dictionary representing a table. Empty dictionary can be passed.

        Returns:
        Dictionary representing of table, in the same form after adding the statistics from games.
        """
        for game in games:
            goals_home = game.result.split("-")[0]
            goals_away = game.result.split("-")[1]
            table = self.__add_stats(table, game.team_home.name,
                                     goals_home=goals_home,
                                     goals_lost_home=goals_away,
                                     matches_home=1)
            table = self.__add_stats(table, game.team_away.name,
                                     goals_away=goals_away,
                                     goals_lost_away=goals_home,
                                     matches_away=1)
            if goals_away > goals_home:
                table = self.__add_stats(table, game.team_away.name, points_away=3, wins_away=1)
                table = self.__add_stats(table, game.team_home.name, loses_home=1)
            elif goals_home > goals_away:
                table = self.__add_stats(table, game.team_home.name, points_home=3, wins_home=1)
                table = self.__add_stats(table, game.team_away.name, loses_away=1)
            elif goals_home == goals_away:
                table = self.__add_stats(table, game.team_home.name, points_home=1, draws_home=1)
                table = self.__add_stats(table, game.team_away.name, points_away=1, draws_away=1)

        table = self.__calculate_total(table)

        return table

    @staticmethod
    def __calculate_total(table):
        for team in table.values():
            team["total_points"] = team["points_home"] + team["points_away"]
            team["total_goals"] = team["goals_home"] + team["goals_away"]
            team["total_goals_lost"] = team["goals_lost_home"] + team["goals_lost_away"]
            team["goal_difference"] = team["total_goals"] - team["total_goals_lost"]
            team["total_wins"] = team["wins_home"] + team["wins_away"]
            team["total_draws"] = team["draws_home"] + team["draws_away"]
            team["total_loses"] = team["loses_home"] + team["loses_away"]
            team["total_matches"] = team["matches_home"] + team["matches_away"]
        return table

    def __count_table(self, table=None, games=None, stat="total_points"):
        """
        Head method of calculating the table. Default running on init with no arguments passed. This means that all
        teams take part in the counting of the table in first iteration. It is later used recursively to calculate
        "minitables" of direct matches between teams that have the same points or goals after the first iteration.
        How it works:
        1. Uses method "count_stats" to calculate statistics after all matches.
           Receives a list of all teams in dictionary with their number of points, goals, matches, etc.
        2. Pass this dict to the "set_positions" method, which returns a list of teams in the order they should be.
           During this method, in case the teams have the same number of points, a recursive "count_table" is run.
        3. Based on the list returned by the previous method, sets teams in the dict to their corresponding positions.

        Keywords Arguments:
        table -- Dictionary representing a table. Empty {} is passed in first iteration. In subsequent iterations,
        only teams for which there is a need to calculate "minitables".
        games -- Games from which the table is counted. By default all matches, in next iterations direct games of teams
        stat -- Argument used in recursion. Specifies according to which statistic it should calculate the table
        for teams that have the same number of points in the head table or after direct matches.

        The method doesn't return anything, it just sets "self.table" attribute to correct table after the calculation.
        """
        first_iteration = False
        if table is None:
            table = self.table
            first_iteration = True
        if games is None:
            games = self.games
        table = self.__count_stats(games, table)
        if first_iteration:
            self.__add_remaining_teams()
        positions = self.__set_positions(table=table, stat=stat)

        table = dict(sorted(table.items(), key=lambda pair: positions.index(pair[0])))
        self.table = table

    def __duplicated_stats(self, stat, table=None):
        """
        A method that segregates teams by number of points or goals.

        Keywords Arguments:
        stat -- Statistic by which teams are to be sorted "total_points" or "total_goals"
        table -- dictionary representing a table.

        Returns:
        Returns a dictionary, where the key is the number of points, value is a list of teams with that amount of points
        """
        dupes = defaultdict(list)
        if table is None:
            table = self.table

        for team, stats in table.items():  # shows teams with the same number of points
            val = stats[stat]
            dupes[val].append(team)

        return dupes

    def __set_position_entire(self, teams):
        mini_table = dict(filter(lambda item: item[0] in teams, self.table.items()))
        mini_table = (sorted(
            mini_table.items(),
            key=lambda x: (x[1]["goal_difference"], x[1]["total_goals"], x[1]["total_wins"], x[1]["wins_away"]),
            reverse=True
        ))
# TODO: more elegant way
        position_list = []
        for team in mini_table:
            position_list.append(team[0])
        return position_list

    def __set_positions(self, table, stat):

        table = dict(sorted(table.items(), key=lambda x: x[1][stat], reverse=True))  # simple sorting by stat
        list_of_position = []
        dupe_points = self.__duplicated_stats(stat, table=table)

        for points, team in dupe_points.items():
            if len(team) == 1:  # if there is one team with a given number of stat
                list_of_position.append(team[0])
            else:
                mini_table = {}
                mini_games = Game.objects.filter(Q(date__range=[self.date_from, self.date_to]) & ~Q(result="None-None")
                                                 & Q(team_home__name__in=team) & Q(team_away__name__in=team))
                if not len(mini_games) == len(team) * 2:  # checks if all matches between the teams have been not played
                    list_of_position = list_of_position + self.__set_position_entire(team)

                elif len(team) < len(table):  # prevents a recursive loop where teams have the same amount of direct stat
                    self.__count_table(table=mini_table, games=mini_games, stat="total_points")  # counts the mini table of direct matches
                elif stat == "total_points":
                    self.__count_table(table=mini_table, games=mini_games, stat="total_goals")
                else:
                    list_of_position = list_of_position + self.__set_position_entire(team)

        return list_of_position

    def tableJSON(self):
        ret = []
        for k, v in self.table.items():
            ret.append({k: v})
            ret[-1][k]["position"] = list(self.table.keys()).index(k)+1
            team = Team.objects.get(name=k)
            ret[-1][k]["team_id"] = team.id
            ret[-1][k]["logo"] = team.logo


        return ret

    def __add_remaining_teams(self):
        if len(self.table) < TEAMS_IN_TABLE:
            teams = Team.objects.filter(~Q(name__in=list(self.table.keys())))
            for team in teams:
                self.table = self.__add_stats(table=self.table, team_name=team.name)

            self.table = self.__calculate_total(self.table)

    def __str__(self):
        return f"Table:({self.date_from} to {self.date_to}"