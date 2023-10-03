from django.db import models
from datetime import datetime, date
from django.db.models import Q

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.CharField(max_length=200, blank=True, null=True)

    imported_from = models.CharField(max_length=200, blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True, default=datetime.now)

    class Meta:
        abstract = True

    @classmethod
    def get_all_imported_id(cls):
        return cls.objects.values_list('imported_from', flat=True)


class Team(BaseModel):
    db_table = 'Team'
    name = models.CharField(max_length=200)
    logo = models.URLField(max_length=200)
    city = models.CharField(max_length=200)
    ekstraklasa = models.BooleanField(default=False)
    founded = models.IntegerField()
    stadium = models.CharField(max_length=200)
    capacity = models.IntegerField()

    class Meta:
        ordering = ['name']

    def finished_games(self):
        return Game.objects.filter(~Q(result="None-None"), Q(team_home=self.id) | Q(team_away=self.id))

    def __str__(self):
        return self.name


class Player(BaseModel):
    db_table = "Player"
    full_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.URLField(max_length=200, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    injured = models.BooleanField(default=False)
    position = models.CharField(max_length=200)
    team = models.ForeignKey(Team, related_name="squad", on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def age(self):
        return int((date.today() - self.birth_date).days / 365.25)

    def __str__(self):
        return self.full_name


class Game(BaseModel):
    db_table = "Game"
    season = models.IntegerField()
    round = models.IntegerField(default=0)
    team_home = models.ForeignKey(Team, related_name="games_home", on_delete=models.SET_NULL, blank=True, null=True)
    team_away = models.ForeignKey(Team, related_name="games_away", on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField()
    halftime = models.CharField(max_length=20)
    result = models.CharField(max_length=20)
    referee = models.CharField(max_length=200, blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True, default=None)
    walkover = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_home} {self.result} {self.team_away}"


class Goal(BaseModel):
    db_table = "Goal"
    scorer = models.ForeignKey(Player, related_name="_player_goals", on_delete=models.SET_NULL, blank=True, null=True)
    assistant = models.ForeignKey(Player, related_name="player_assists", on_delete=models.SET_NULL, blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    minute_extra = models.IntegerField(blank=True, null=True)
    team_scored = models.ForeignKey(Team, related_name="team_goals", on_delete=models.SET_NULL, blank=True, null=True)
    team_against = models.ForeignKey(Team, related_name="team_goals_lost", on_delete=models.SET_NULL, blank=True, null=True)
    # replay =
    penalty = models.BooleanField(default=False)
    own_goal = models.BooleanField(default=False)
    own_goal_scorer = models.ForeignKey(Player, related_name="_player_own_goals", on_delete=models.SET_NULL, blank=True, null=True, default=None)
    game = models.ForeignKey(Game, related_name="game_goals", on_delete=models.CASCADE, blank=True, null=True)
