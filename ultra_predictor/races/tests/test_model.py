from ultra_predictor.races.models import RaceGroup
from ultra_predictor.races.tests.factories import RaceFactory, RunnerFactory

import pytest


@pytest.fixture
def race():
    return RaceFactory()


@pytest.fixture
def runner():
    return RunnerFactory()


def test_race_group_string():
    race_group = RaceGroup(name="Wielka Prehyba")
    assert str(race_group) == "Wielka Prehyba"


def test_race_string(db, race):
    name = race.name
    assert str(race) == name


def test_runner_string(db, runner):
    name = runner.name
    birth_year = runner.birth_year
    assert str(runner) == f"{name}, {birth_year}"
