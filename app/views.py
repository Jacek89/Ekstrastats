from django.shortcuts import render
from .models import Team, Player, Game, Goal
from .utils.table import table
from .utils.statistics import count_intervals, count_score_stats
from .utils.general import summary_post, flag
from django.http import JsonResponse
from .forms import TableDate
from django.views import View
from django.db.models import Count, Q, Min, Max, F, Prefetch
from Ekstrastats.settings.settings import SEASON

from collections import defaultdict


def index(request):
    rounds = Game.objects.values('round').annotate(
        num_games=Count('id', distinct=True),
        num_goals=Count('game_goals', distinct=True),
        first_game_date=Min('date'),
        last_game_date=Max('date')
    ).order_by('-round')

    context = {
        'rounds': rounds
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
    games = team.finished_games().select_related("team_home", "team_away").prefetch_related(
        Prefetch("game_goals", queryset=Goal.objects.select_related("scorer", "team_scored", "own_goal_scorer"))
    ).order_by("-date")

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
    scorers = Player.objects.annotate(goals_count=Count('player_goals')
                                      ).select_related("team").order_by('-goals_count', 'last_name')[:5]
    assists = Player.objects.annotate(assists_count=Count('player_assists')
                                      ).select_related("team").order_by('-assists_count', 'last_name')[:5]
    canadian = Player.objects.annotate(
        canadian_count=Count('player_goals', distinct=True) + Count('player_assists', distinct=True)
    ).select_related("team").order_by('-canadian_count', 'last_name')[:5]

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
    flag_iso = flag(player.nationality)

    context = {
        "player": player,
        'flag': flag_iso
    }

    return render(request, "app/player.html", context)


def round_summary(request, round_num):

    games = Game.objects.filter(round=round_num).select_related("team_home", "team_away").prefetch_related(
        Prefetch("game_goals", queryset=Goal.objects.select_related("scorer", "team_scored", "own_goal_scorer"))
    ).order_by("date")

    stats = games.annotate(
        total_goals=Count('game_goals__id'),
        first_goal_minute=Min('game_goals__minute')
    ).aggregate(
        total_goals=Count('game_goals__id'),
        first_goal_minute=Min('game_goals__minute')
    )

    num_games = len(games)
    goals_per_game = round(stats['total_goals'] / num_games, 2)
    score_stats = count_score_stats(games)

    players_stats = Player.objects.annotate(
        goals=Count('player_goals__id', filter=Q(player_goals__game__round=round_num), distinct=True),
        assists=Count('player_assists__id', filter=Q(player_assists__game__round=round_num), distinct=True),
    ).annotate(
        combined_goals_assists=F('goals') + F('assists')
    ).filter(combined_goals_assists__gt=1).order_by('-combined_goals_assists', '-goals', '-assists', 'last_name')

    own_goals = Player.objects.annotate(own_goals=Count(
            'player_own_goals__id', filter=Q(player_own_goals__game__round=round_num), distinct=True
            )).filter(own_goals__gt=0).select_related('team')

    context = {
        'round_num': round_num,
        'num_games': num_games,
        'games': games,
        'total_goals': stats['total_goals'],
        'goals_per_game': goals_per_game,
        'first_goal_minute': stats['first_goal_minute'],
        'players_stats': players_stats,
        'own_goals': own_goals,
        'score_stats': score_stats,
        'summary_post': summary_post(round_num=round_num, num_games=num_games, goals=stats['total_goals'],
                                     gpm=goals_per_game, score_stats=score_stats, own_goals=own_goals)
    }

    return render(request, 'app/round.html', context)

