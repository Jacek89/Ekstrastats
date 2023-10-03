from django.shortcuts import render
from .models import Team
from .utils.table import TableCounter


def index(request):

    contex = {

    }

    return render(request, "app/home.html", contex)


def table(request):

    tablek = TableCounter().tableJSON()
    for row in tablek:
        team = next(iter(row))
        team = Team.objects.get(name=team)
        row[team.name]["team_id"] = team.id
        row[team.name]["logo"] = team.logo

    contex = {
        "table": tablek
    }

    return render(request, "app/table.html", contex)


def team_main(request, team_id):

    contex = {
        "team": Team.objects.get(id=team_id)
    }

    return render(request, "app/team.html", contex)
