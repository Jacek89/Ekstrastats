from django.shortcuts import render
from .models import Team, Player, Game
from .utils.table import TableCounter
from django.http import JsonResponse
from .forms import TableDate
from django.core.cache import cache
from django.views import View


def index(request):

    contex = {

    }

    return render(request, "app/home.html", contex)


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
        players[position] = Player.objects.filter(team=team, position=position)

    contex = {
        "team": team,
        "players": players,
        "games": games
    }

    return render(request, "app/team.html", contex)
