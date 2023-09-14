import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ekstrastats.settings')
django.setup()

from app.models import Team
import requests


URL = "https://v3.football.api-sports.io"
API_KEY = os.environ.get("RAPID_API_KEY")
LEAGUE_ID = 106
header = {"x-rapidapi-key": API_KEY}
params = {"league": LEAGUE_ID,
          "season": 2023}

response = requests.get(url=f"{URL}/teams", params=params, headers=header)
data = response.json()


def add_teams():
    for team in data['response']:
        Team.objects.create(
            name=team['team']['name'],
            logo=team['team']['logo'],
            city=team['venue']['city'],
            founded=team['team']['founded'],
            stadium=team['venue']['name'],
            capacity=team['venue']['capacity'],
            imported_from=str('AF#' + str(team['team']['id'])),
        )

add_teams()