from django.shortcuts import render
from .models import Team


def index(request):

    contex = {

    }

    return render(request, "app/home.html", contex)


def table(request):

    contex = {

    }

    return render(request, "app/table.html", contex)


def team_main(request, team_id):

    contex = {
        "team": Team.objects.get(id=team_id),

    }

    return render(request, "app/team.html", contex)
