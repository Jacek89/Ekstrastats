from django.shortcuts import render
from .models import Team
from .utils.table import TableCounter
from django.http import JsonResponse
from .forms import TableDate
from django.core.cache import cache


def index(request):

    contex = {

    }

    return render(request, "app/home.html", contex)


def table(request):

    contex = {
        "form": TableDate()
    }

    return render(request, "app/table.html", contex)


def process_table(request):

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if date_to is None and date_from is None:
        if cache.get('table') is None:
            tablek = TableCounter().tableJSON()
            cache.add("table", tablek, 10000)
        else:
            tablek = cache.get('table')
    else:
        tablek = TableCounter(date_from=date_from, date_to=date_to).tableJSON()

    response = {
        "data": tablek
    }
    return JsonResponse(response)


def team_main(request, team_id):

    contex = {
        "team": Team.objects.get(id=team_id)
    }

    return render(request, "app/team.html", contex)
