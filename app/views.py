from django.shortcuts import render
from .models import Team, Player, Game, Goal
from .utils.table import TableCounter
from django.http import JsonResponse
from .forms import TableDate
from django.core.cache import cache
from django.views import View
from django.db.models import Count
from Ekstrastats.settings.settings import SEASON
from .utils.statistics import count_intervals


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

            if date_to is None and date_from is None:
                if cache.get('table') is None:
                    tablek = TableCounter().tableJSON()
                    cache.add("table", tablek, 600000)  # one week
                else:
                    tablek = cache.get('table')
            else:
                tablek = TableCounter(date_from=date_from, date_to=date_to).tableJSON()

            response = {
                "data": tablek
            }
            return JsonResponse(response)

        return render(request, self.template_name, {"form": form})


def team_main(request, team_id):
    team = Team.objects.get(id=team_id)
    players = {}
    games = team.finished_games().order_by("-date")
    for position in ["Goalkeeper", "Defender", "Midfielder", "Attacker"]:
        players[position] = Player.objects.filter(team__id=team_id, position=position)

    context = {
        "team": team,
        "players": players,
        "games": games
    }

    return render(request, "app/team.html", context)


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

