import os
import pytest


from ultra_predictor.races.tests.factories import (
    PredictionRaceGroupFactory,
    PredictionRaceFactory,
    RunnerFactory,
    PredictionRaceResultFactory,
    HistoricalRaceFactory,
    HistoricalRaceResultFactory,
)

CURRENT_APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def runner():
    return RunnerFactory()


@pytest.fixture
def prediction_race_group():
    return PredictionRaceGroupFactory()


@pytest.fixture
def prediction_race():
    return PredictionRaceFactory()


@pytest.fixture
def prediction_race_result():
    return PredictionRaceResultFactory()


@pytest.fixture
def historical_race():
    return HistoricalRaceFactory()


@pytest.fixture
def historical_race_result():
    return HistoricalRaceResultFactory()


@pytest.fixture
def itra_html():
    with open(CURRENT_APP_PATH+"/tests/fixtures/itra_race.html") as f:
        html = f.read()
    return html

@pytest.fixture
def itra_runner_profile_html():
    with open(CURRENT_APP_PATH+"/tests/fixtures/itra_runner_year.html") as f:
        html = f.read()
    return html


@pytest.fixture
def eduhub_page_html_1():
    with open(CURRENT_APP_PATH+"/tests/fixtures/endu_hube_result_page_1.html") as f:
        html = f.read()
    return html