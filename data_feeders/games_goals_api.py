import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ekstrastats.settings')
django.setup()

from app.models import Goal, Player, Game, Team
import requests
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

URL = "https://v3.football.api-sports.io"
API_KEY = os.environ.get("RAPID_API_KEY")
LEAGUE_ID = 106
SEASON = 2023

header = {"x-rapidapi-key": API_KEY}


def get_games(round=None, d_from=None, d_to=None):
    if round is not None:
        params_fixtures = {"league": LEAGUE_ID,
                           "season": SEASON,
                           "round": f'Regular Season - {round}'}
    elif d_from is not None and d_to is not None:
        params_fixtures = {"from": d_from,
                           "to": d_to,
                           "league": LEAGUE_ID,
                           "season": SEASON}
    else:
        return "Wrong values are given"
    response_fixture = requests.get(url=f"{URL}/fixtures", params=params_fixtures, headers=header).json()
    for game in response_fixture['response']:
        walkover = False
        import_id = f"AF#{game['fixture']['id']}"
        referee = game['fixture']['referee']
        season = game['league']['season']
        date = datetime.fromtimestamp(game['fixture']['timestamp'])
        team_home = f"AF#{game['teams']['home']['id']}"
        team_away = f"AF#{game['teams']['away']['id']}"

        halftime = f"{game['score']['halftime']['home']}-{game['score']['halftime']['away']}"
        result = f"{game['score']['fulltime']['home']}-{game['score']['fulltime']['away']}"
        if game['fixture']['status']['short'] == "WO":
            walkover = True

        Game.objects.create(
            season=season,
            round=round if round else game['league']['round'].split("-")[1],
            team_home=Team.objects.get(imported_from=team_home),
            team_away=Team.objects.get(imported_from=team_away),
            date=date,
            halftime=halftime,
            result=result,
            referee=referee,
            walkover=walkover,
            imported_from=import_id
        )
        get_events(game['fixture']['id'], game['teams']['home']['id'], game['teams']['away']['id'])


def get_events(id_fixture: int, id_team1: int, id_team2: int):
    params_events = {"fixture": id_fixture}
    response_events = requests.get(url=f"{URL}/fixtures/events", params=params_events, headers=header).json()

    for event in response_events['response']:
        scorer = None
        assistant = None
        minute = None
        minute_extra = None
        team_scored = None
        team_against = None
        penalty = False
        own_goal = False
        own_goal_scorer = None
        game = None
        if event['type'] == 'Goal' and event['detail'] != "Missed Penalty":
            minute = event['time']['elapsed']
            if event['time']['extra']:
                minute_extra = event['time']['extra']
            game = f"AF#{id_fixture}"
            if event['assist']['id']:
                assistant = f"AF#{event['assist']['id']}"
            team_scored = f"AF#{event['team']['id']}"
            if int(event['team']['id']) == id_team1:
                team_against = f"AF#{id_team2}"
            else:
                team_against = f"AF#{id_team1}"
            if event['detail'] == "Penalty" or event['detail'] == "Normal Goal":
                scorer = f"AF#{event['player']['id']}"
                if event['detail'] == "Penalty":
                    penalty = True
            if event['detail'] == "Own Goal":
                own_goal = True
                own_goal_scorer = f"AF#{event['player']['id']}"

            try:
                Goal.objects.create(
                    scorer=Player.objects.get(imported_from=scorer) if scorer else None,
                    assistant=Player.objects.get(imported_from=assistant) if assistant else None,
                    minute=minute,
                    minute_extra=minute_extra,
                    team_scored=Team.objects.get(imported_from=team_scored),
                    team_against=Team.objects.get(imported_from=team_against),
                    penalty=penalty,
                    own_goal=own_goal,
                    own_goal_scorer=Player.objects.get(imported_from=own_goal_scorer) if own_goal_scorer else None,
                    game=Game.objects.get(imported_from=game),
                    imported_from=f"AF#fixture#{id_fixture}"
                )
            except ObjectDoesNotExist:
                print(f"GOAL IMPORT FAILED: fixture: {id_fixture}, minute: {minute}")

