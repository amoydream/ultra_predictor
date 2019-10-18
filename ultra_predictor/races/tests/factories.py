from typing import Any, Sequence
from decimal import Decimal
from ultra_predictor.users.models import User
from factory import DjangoModelFactory, Faker, SubFactory, PostGenerationMethodCall


from ultra_predictor.races.models import RaceGroup, Race, Runner, RaceResult


class RaceGroupFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = RaceGroup
        django_get_or_create = ["name"]


class RaceFactory(DjangoModelFactory):

    name = Faker("bs")
    start_date = Faker("date")
    distance = Decimal("64.4")
    elevation_gain = 1300
    elevation_lost = 1300
    itra = 3
    itra_race_id = 12934
    food_point = 3
    time_limit = Decimal("9.5")
    race_group = SubFactory(RaceGroupFactory)

    class Meta:
        model = Race
        django_get_or_create = ["name"]


class RunnerFactory(DjangoModelFactory):

    name = Faker("name")
    birth_year = Faker("random_int", min=1965, max=2000)

    class Meta:
        model = Runner
        django_get_or_create = ["name", "birth_year"]


class RaceResultFactory(DjangoModelFactory):
    race = SubFactory(RaceFactory)
    runner = SubFactory(RunnerFactory)
    time_result = Faker("time_delta", end_datetime=1)

    class Meta:
        model = RaceResult
        django_get_or_create = ["race", "runner"]

