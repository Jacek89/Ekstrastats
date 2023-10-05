from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("table/", views.table, name="table"),
    path('team/<int:team_id>/', views.team_main, name="team_main"),
    path('process_table/', views.process_table, name="process_table"),
]