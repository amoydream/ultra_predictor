from ultra_predictor.races.models import RaceGroup
from ultra_predictor.races.tests.factories import (
    RaceGroupFactory,
    RaceFactory,
    RunnerFactory,
    RaceResultFactory,
)

import pytest


@pytest.fixture
def race():
    return RaceFactory()


@pytest.fixture
def runner():
    return RunnerFactory()


@pytest.fixture
def race_group():
    return RaceGroupFactory()


@pytest.fixture
def race_result():
    return RaceResultFactory()


def test_race_group_string(db, race_group):
    assert str(race_group) == race_group.name


def test_race_string(db, race):
    name = race.name
    assert str(race) == name


def test_runner_string(db, runner):
    name = runner.name
    birth_year = runner.birth_year
    assert str(runner) == f"{name}, {birth_year}"


def test_race_results_string(db, race_result):
    assert (
        str(race_result)
        == f"{race_result.runner.name}, {race_result.race.name}, {race_result.time_result}"
    )
