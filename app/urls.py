from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("table/", views.TableView.as_view(), name="table"),
    path('team/<int:team_id>', views.team_main, name="team_main"),
    path('team_statistics/<int:team_id>', views.team_stats, name="team_stats"),
    path('statistics/', views.statistics, name="statistics"),
    path('player/<int:player_id>/', views.player_main, name="player_main")
]