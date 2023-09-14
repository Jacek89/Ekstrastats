import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ekstrastats.settings')
django.setup()

from app.models import Team, Player
import requests

URL = "https://v3.football.api-sports.io"
API_KEY = os.environ.get("RAPID_API_KEY")

header = {"x-rapidapi-key": API_KEY}

def drop_units(str):
    if str:
        return str.split(' ')[0]
    else:
        return None

def get_all_players(teams):
    for team_id in teams:
        page = 1
        while True:
            params = {"team": team_id[3:],
                      "season": 2023,
                      'page': page}
            response = requests.get(url=f"{URL}/players", params=params, headers=header).json()

            for player in response['response']:
                Player.objects.create(
                    full_name=player['player']['name'],
                    first_name=player['player']['firstname'],
                    last_name=player['player']['lastname'],
                    nationality=player['player']['nationality'],
                    photo=player['player']['photo'],
                    height=drop_units(player['player']['height']),
                    weight=drop_units(player['player']['weight']),
                    position=player['statistics'][0]['games']['position'],
                    birth_date=datetime.strptime(player['player']['birth']['date'], '%Y-%m-%d').date(),
                    imported_from=str('AF#' + str(player['player']['id'])),
                    team=Team.objects.get(imported_from=team_id)
                )

            if response['paging']['total'] > page:
                page += 1
            else:
                break


teams = Team.get_all_imported_id()

get_all_players(teams)
