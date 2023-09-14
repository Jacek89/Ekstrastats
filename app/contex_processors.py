from .models import Team


def teams_extra(request):
    teams = Team.objects.filter(ekstraklasa=True)
    return {'teams_extra': teams}

