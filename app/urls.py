from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("table/", views.TableView.as_view(), name="table"),
    path('team/<int:team_id>', views.team_main, name="team_main"),
    path('team_statistics/<int:team_id>', views.team_stats, name="team_stats"),
    path('statistics/', views.statistics, name="statistics"),
    path('player/<int:player_id>/', views.player_main, name="player_main"),
    path('round/<int:round_num>', views.round_summary, name="round"),
    path('analysis', views.analysis_main, name="analysis"),
    path('analysis_pois/<int:team_home>/<int:team_away>/', views.analysis_poisson, name="analysis_pois")
]
