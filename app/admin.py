from django.contrib import admin

from .models import Player, Team, Game, Goal

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Goal)
