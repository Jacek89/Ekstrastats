from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("table/", views.TableView.as_view(), name="table"),
    path('team/<int:team_id>/', views.team_main, name="team_main"),
]