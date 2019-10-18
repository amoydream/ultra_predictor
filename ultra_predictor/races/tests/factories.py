from typing import Any, Sequence
from decimal import Decimal
from ultra_predictor.users.models import User
from factory import DjangoModelFactory, Faker, SubFactory, PostGenerationMethodCall


from ultra_predictor.races.models import RaceGroup, Race


class RaceGroupFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = RaceGroup
        django_get_or_create = ["name"]


class RaceFactory(DjangoModelFactory):

    name = Faker("name")
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
