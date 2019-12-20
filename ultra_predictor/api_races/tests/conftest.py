import pytest
from django.contrib.auth import get_user_model
from ultra_predictor.races.tests.factories import PredictionRaceFactory


@pytest.fixture
def event_payload():
    return dict(name="Wielka prehyba", year=2019, itra_id="123")


@pytest.fixture
def race_payload():
    pred_race = PredictionRaceFactory(event=None)
    keys_i_want = [
        "name",
        "itra_event_id",
        "itra_race_id",
        "itra_point",
        "mount_point",
        "finish_point",
        "map_link",
        "participation",
        "sentiers",
        "pistes",
        "routes",
        "challenge",
        "championship",
        "country_start",
        "city_start",
        "country_finish",
        "city_finish",
        "distance",
        "race_date",
        "race_time",
        "ascent",
        "descent",
        "refreshment_points",
        "max_time",
    ]
    race = {my_key: str(vars(pred_race)[my_key]) for my_key in keys_i_want}

    return race


@pytest.fixture
def current_user():
    user = get_user_model().objects.create_user("test@mojek.pl", "pass123")
    return user
