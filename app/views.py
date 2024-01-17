from django.shortcuts import render
from .models import Team, Player, Game, Goal
from .utils.table import table
from django.http import JsonResponse
from .forms import TableDate
from django.views import View
from django.db.models import Count, Q
from Ekstrastats.settings.settings import SEASON
from .utils.statistics import count_intervals
from collections import defaultdict


def index(request):
    context = {

    }

    return render(request, "app/home.html", context)


class TableView(View):
    template_name = "app/table.html"
    form_class = TableDate

    def get(self, request):
        form = self.form_class()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            date_to = request.GET.get('date_to')
            date_from = request.GET.get('date_from')

            response = {
                "data": table(date_from=date_from, date_to=date_to)
            }
            return JsonResponse(response)

        return render(request, self.template_name, {"form": form})


def team_main(request, team_id):
    team = Team.objects.get(id=team_id)
    games = team.finished_games().select_related("team_home", "team_away").order_by("-date")

    players = defaultdict(list)
    players_query = Player.objects.filter(team__id=team_id).select_related("team")
    for x in players_query:
        players[x.position].append(x)
    position_index = ["Goalkeeper", "Defender", "Midfielder", "Attacker"]

    context = {
        "tab": request.GET.get('tab') if request.GET.get('tab') is not None else 'overview',
        "team": team,
        "players": dict(sorted(players.items(), key=lambda y: position_index.index(y[0]))),
        "games": games
    }

    return render(request, "app/team.html", context)


def team_stats(request, team_id):
    team = Team.objects.get(id=team_id)
    players_query = Player.objects.filter(team__id=team_id).select_related("team")

    scorers = players_query.annotate(goals_count=Count('player_goals')).order_by('-goals_count')[:5]
    assistants = players_query.annotate(assists_count=Count('player_assists')).order_by('-assists_count')[:5]
    canadian = players_query.annotate(
        canadian_count=Count('player_goals', distinct=True) + Count('player_assists', distinct=True)
    ).order_by('-canadian_count')[:5]

    over25 = Game.objects.filter(Q(team_away_id=team_id) | Q(team_home_id=team_id)).annotate(
        total_goals=Count('game_goals__id')).filter(total_goals__gt=2).count()

    clean_sheets = team.finished_games().exclude(Q(team_away_id=team_id, game_goals__team_against_id=team_id) |
                                                 Q(team_home_id=team_id, game_goals__team_against_id=team_id)).count()

    failed_to_score = team.finished_games().exclude(Q(team_away_id=team_id, game_goals__team_scored_id=team_id) |
                                                    Q(team_home_id=team_id, game_goals__team_scored_id=team_id)).count()

    context = {
        'failed_to_score': failed_to_score,
        'clean_sheets': clean_sheets,
        'over25': over25,
        'tab': next(i[team.name] for i in table() if team.name in i),
        'team': team,
        'scorers': scorers,
        'assistants': assistants,
        'canadian': canadian
    }

    return render(request, "app/team_stats.html", context)


def statistics(request):
    scorers = Player.objects.annotate(goals_count=Count('player_goals')).order_by('-goals_count')[:5]
    assists = Player.objects.annotate(assists_count=Count('player_assists')).order_by('-assists_count')[:5]
    canadian = Player.objects.annotate(
        canadian_count=Count('player_goals', distinct=True) + Count('player_assists', distinct=True)
    ).order_by('-canadian_count')[:5]

    goal_minutes = Goal.objects.filter(game__season=SEASON).values_list('minute', flat=True)
    all_games = Game.objects.filter(season=SEASON).count()
    goals_15 = dict(count_intervals(goal_minutes, [15, 30, 45, 60, 75, 90]))
    goals_45 = dict(count_intervals(goal_minutes, [45, 90]))
    goals_sum = sum(goals_45.values())

    context = {
        "scorers": scorers,
        "assists": assists,
        "canadian": canadian,
        "goals_15": goals_15,
        "goals_45": goals_45,
        "goals_sum": goals_sum,
        "goals_per_game": round(len(goal_minutes) / all_games, 2)
    }

    return render(request, "app/statistics.html", context)


def player_main(request, player_id):
    player = Player.objects.get(id=player_id)

    context = {
        "player": player
    }

    return render(request, "app/player.html", context)
