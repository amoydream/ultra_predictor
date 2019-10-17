from ultra_predictor.races.models import RaceGroup
from ultra_predictor.races.tests.factories import RaceFactory

import pytest


@pytest.fixture
def race():
    return RaceFactory()


def test_race_group_string():
    race_group = RaceGroup(name="Wielka Prehyba")
    assert str(race_group) == "Wielka Prehyba"


def test_race_string(db, race):
    name = race.name
    assert str(race) == name
