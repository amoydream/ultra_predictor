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
    start_date = Faker("date")
    end_date = Faker("date")
    future_event = False

    class Meta:
        model = Event
        django_get_or_create = ["name"]


class PredictionRaceGroupFactory(DjangoModelFactory):

    name = Faker("name")
    
    class Meta:
        model = PredictionRaceGroup
        django_get_or_create = ["name"]


class PredictionRaceFactory(DjangoModelFactory):
    name = Faker("name")
    start_date = Faker("date")
    distance = Decimal("64.4")
    elevation_gain = 1300
    elevation_lost = 1300
    itra = 3
    itra_race_id = 12934
    food_point = 3
    event = SubFactory(EventFactory)
    time_limit = Decimal("9.5")
    prediction_race_group = SubFactory(PredictionRaceGroupFactory)

    class Meta:
        model = PredictionRace
        django_get_or_create = ["name"]


class RunnerFactory(DjangoModelFactory):

    first_name = Sequence(lambda n: f"runner_first_name_{n}")
    last_name = Sequence(lambda n: f"runner_last_name_{n}")
    birth_year = Faker("random_int", min=1965, max=2000)
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
    start_date = Faker("date")
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
