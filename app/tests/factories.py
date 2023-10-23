import django
import os

import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ekstrastats.settings.settings')
django.setup()


from app.models import Team, Player, Game, Goal
import factory.fuzzy
from datetime import date, datetime


class TeamModelFactory(factory.django.DjangoModelFactory):
    club_names = ["Pogoń", "Górnik", "Lechia", "KS", "Zagłębie", "Wisła", "GKS", "Skra", "Hutnik", "Polonia", "Warta",
                  "Unia", "Flota", "Odra", "Garbarnia", "Sokół", "Azoty", "Trefl", "Czarni", "Piast", "Zenit", "Stal",
                  "Syrenka", "Spójna", "Korona", "Sparta", "Hetman", "Kuźnia", "Kotwica", "Start", "Lider", "Omega",
                  "Victoria", "Fortuna", "Gryf", "Arka", "Grom", "Chemik", "Orzeł", "Iskra", "Olimp", "Błękitni",
                  "Ruch", "Znicz", "Rozwój", "Tęcza", "Motor", "Metal", "Orkan", "Legion", "Świt", "Gwiazda", "Zryw",
                  "Tempo", "Zawisza", "Strumyk", "Przebój", "Błysk", "Puszcza", "Olimpia", "Jutrzenka", "Jastrząb"]
    class Meta:
        model = Team
        exclude = ('club_names', "club_name")

    class Params:
        fake_name = factory.Faker('name_male', locale='pl_PL')
        fake_address = factory.Faker('street_address', locale='pl_PL')

    city = factory.Faker('city', locale='pl_PL')
    club_name = factory.fuzzy.FuzzyChoice(club_names)
    name = factory.LazyAttribute(lambda a: f"{a.club_name} {a.city}")
    logo = factory.Faker('image_url')
    ekstraklasa = True
    founded = factory.fuzzy.FuzzyInteger(1905, 1950)
    stadium = factory.LazyAttribute(lambda a: f"Stadion im. {a.fake_name}, {a.fake_address}")
    capacity = factory.fuzzy.FuzzyInteger(4500, 58580)


class PlayerModelFactory(factory.django.DjangoModelFactory):
    locale = factory.fuzzy.FuzzyChoice(["cs_CZ", "da_DK", "de_DE", "en_GB", "es_ES", "fr_FR", "hr_HR", "hu_HU",
                                        "it_IT", "nl_NL", "no_NO", "pt_BR", "pt_PT", "ro_RO", "sk_SK", "fr_CH",
                                        "de_AT", "es_AR", "pl_PL"])
    class Meta:
        model = Player
        exclude = ("locale",)

    first_name = factory.Faker("first_name_male", locale=locale)
    last_name = factory.Faker("last_name_male", locale=locale)
    full_name = factory.LazyAttribute(lambda o: f"{o.first_name} {o.last_name}")
    nationality = factory.Faker("current_country", locale=locale)
    birth_date = factory.fuzzy.FuzzyDate(
        start_date=date.today().replace(year=date.today().year - 35),
        end_date=date.today().replace(year=date.today().year - 16)
    )
    photo = factory.Faker('image_url')
    height = factory.fuzzy.FuzzyInteger(160, 210)
    weight = factory.fuzzy.FuzzyInteger(65, 92)
    injured = False
    position = factory.fuzzy.FuzzyChoice(["Goalkeeper", "Defender", "Midfielder", "Attacker"])
    team = factory.SubFactory(TeamModelFactory)


class GameModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    class Params:
        goals_team_home = factory.fuzzy.FuzzyInteger(0, 4)
        goals_team_away = factory.fuzzy.FuzzyInteger(0, 4)
        date_unaware = factory.fuzzy.FuzzyDate(start_date=date(2023, 7, 20), end_date=date.today())
        stadium_fill = factory.fuzzy.FuzzyDecimal(0.1, 1, 3)

    season = 2023
    round = 1
    team_home = factory.SubFactory(TeamModelFactory)
    team_away = factory.SubFactory(TeamModelFactory)
    date = factory.LazyAttribute(lambda o: datetime.combine(o.date_unaware, datetime.min.time()).replace(tzinfo=pytz.UTC))
    halftime = factory.LazyAttribute(lambda o: f"{o.goals_team_home // 2}-{o.goals_team_away // 2}")
    result = factory.LazyAttribute(lambda o: f"{o.goals_team_home}-{o.goals_team_away}")
    referee = factory.Faker('name_male', locale='pl_PL')
    attendance = factory.LazyAttribute(lambda o: int(o.team_home.capacity * o.stadium_fill))
    walkover = False



# game = GameModelFactory.build()
# print(game.team_home.name)
# print(game.team_away.name)
# print(game.halftime)
# print(game.result)
# print(game.referee)
# print(game.attendance)
# print(game.date)

class GoalModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    class Params:
        minut = factory.fuzzy.FuzzyInteger(0, 90)
        extra_minute = factory.fuzzy.FuzzyChoice(["None", 1, 2, 3, 4, 5])
        pen = factory.fuzzy.FuzzyInteger(1, 10)

    scorer = factory.SubFactory(PlayerModelFactory)
    assistant = factory.SubFactory(PlayerModelFactory)
    minute = factory.LazyAttribute(lambda o: o.minut)
    team_scored = factory.SubFactory(TeamModelFactory)
    team_against = factory.SubFactory(TeamModelFactory)
    own_goal = False
    own_goal_scorer = None
    game = factory.SubFactory(GameModelFactory)

    @factory.lazy_attribute
    def minute_extra(self):
        if self.minut == 45 or self.minut == 90:
            return self.extra_minute
        else:
            return None

    @factory.lazy_attribute
    def penalty(self):
        if self.pen == 1:
            return True
        else:
            return False



# goal = GoalModelFactory.build()
# print(goal.team_scored)
# print(goal.team_against)
# print(goal.minute)
# print(goal.minute_extra)
# print(goal.penalty)