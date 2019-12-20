from decimal import Decimal
from ultra_predictor.users.models import User
from factory import (
    DjangoModelFactory,
    Faker,
    SubFactory,
    PostGenerationMethodCall,
    Sequence,
)


from ultra_predictor.races.models import (
    Event,
    PredictionRaceGroup,
    PredictionRace,
    Runner,
    PredictionRaceResult,
    HistoricalRace,
    HistoricalRaceResult,
)


class EventFactory(DjangoModelFactory):

    name = Sequence(lambda n: f"event_{n}")
    year = Faker("random_int", min=2015, max=2019)
    itra_id = Faker("random_int", min=1, max=1000)
    future_event = False

    class Meta:
        model = Event
        django_get_or_create = ["name", "year"]


class PredictionRaceGroupFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = PredictionRaceGroup
        django_get_or_create = ["name"]


class PredictionRaceFactory(DjangoModelFactory):
    name = Faker("name")
    itra_event_id = Faker("random_int", min=1, max=1000)
    itra_race_id = Faker("random_int", min=1, max=1000)
    itra_point = Faker("random_int", min=1, max=5)
    mount_point = Faker("random_int", min=1, max=5)
    finish_point = Faker("random_int", min=1, max=5)
    map_link = Faker("uri")
    participation = "solo"
    sentiers = Faker("random_int", min=1, max=100)
    pistes = Faker("random_int", min=1, max=100)
    routes = Faker("random_int", min=1, max=100)
    challenge = Faker("name")
    championship = Faker("name")
    country_start = Faker("country")
    city_start = Faker("city")
    country_finish = Faker("country")
    city_finish = Faker("city")
    race_date = Faker("date_between", start_date="-2y", end_date="-1y")
    race_time = Faker("time_object")
    distance = Faker("random_int", min=65, max=100)
    ascent = Faker("random_int", min=1000, max=4000)
    descent = Faker("random_int", min=1000, max=4000)

    refreshment_points = Faker("random_int", min=1, max=5)
    event = SubFactory(EventFactory)
    max_time = Faker("time_delta", end_datetime=1)
    prediction_race_group = SubFactory(PredictionRaceGroupFactory)

    class Meta:
        model = PredictionRace
        django_get_or_create = ["name"]


class RunnerFactory(DjangoModelFactory):

    first_name = Sequence(lambda n: f"runner_first_name_{n}")
    last_name = Sequence(lambda n: f"runner_last_name_{n}")
    birth_year = Faker("random_int", min=1965, max=2000)
    sex = Faker("random_element", elements=("w", "m"))
    nationality = Faker("country")

    class Meta:
        model = Runner
        django_get_or_create = ["first_name", "last_name", "birth_year"]


class PredictionRaceResultFactory(DjangoModelFactory):
    prediction_race = SubFactory(PredictionRaceFactory)
    runner = SubFactory(RunnerFactory)
    time_result = Faker("time_delta", end_datetime=1)
    position = Sequence(lambda n: n)

    class Meta:
        model = PredictionRaceResult
        django_get_or_create = ["prediction_race", "runner"]


class HistoricalRaceFactory(DjangoModelFactory):
    name = Faker("name")
    start_date = Faker("date_between", start_date="-30y", end_date="-1y")
    distance = Decimal("64.4")

    class Meta:
        model = HistoricalRace
        django_get_or_create = ["name"]


class HistoricalRaceResultFactory(DjangoModelFactory):
    historical_race = SubFactory(HistoricalRaceFactory)
    runner = SubFactory(RunnerFactory)
    time_result = Faker("time_delta", end_datetime=1)

    class Meta:
        model = HistoricalRaceResult
        django_get_or_create = ["historical_race", "runner"]
