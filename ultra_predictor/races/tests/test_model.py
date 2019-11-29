# from ultra_predictor.races.models import PredictionRaceGroup
import pytest
from decimal import Decimal
from .factories import (
    PredictionRaceGroupFactory,
    PredictionRaceFactory,
    PredictionRaceResultFactory,
    RunnerFactory,
    HistoricalRaceFactory,
    HistoricalRaceResultFactory,
)


def test_runner_string(db, runner):
    name = runner.name
    birth_year = runner.birth_year
    assert str(runner) == f"{name}, {birth_year}"


def test_race_group_string(db, prediction_race_group):
    assert str(prediction_race_group) == prediction_race_group.name


def test_prediction_race_string(db, prediction_race):
    name = prediction_race.name
    assert str(prediction_race) == name


def test_prediction_race_results_string(db, prediction_race_result):
    assert (
        str(prediction_race_result) == f"{prediction_race_result.runner.name}, "
        f"{prediction_race_result.prediction_race.name}, "
        f"{prediction_race_result.time_result}"
    )


def test_historiacal_race_string(db, historical_race):
    name = historical_race.name
    assert str(historical_race) == name


def test_historical_race_results_string(db, historical_race_result):
    assert (
        str(historical_race_result) == f"{historical_race_result.runner.first_name} "
        f"{historical_race_result.runner.last_name}, "
        f"{historical_race_result.historical_race.name}, "
        f"{historical_race_result.time_result}"
    )


def test_all_results_of_prediction_races_of_race_group(db):
    group1 = PredictionRaceGroupFactory()
    group2 = PredictionRaceGroupFactory()
    race1 = PredictionRaceFactory(prediction_race_group=group1)
    race2 = PredictionRaceFactory(prediction_race_group=group1)
    race3 = PredictionRaceFactory(prediction_race_group=group2)
    PredictionRaceResultFactory.create_batch(10, prediction_race=race1)
    PredictionRaceResultFactory.create_batch(10, prediction_race=race2)
    PredictionRaceResultFactory.create_batch(10, prediction_race=race3)

    assert len(group1.all_results_of_prediction_races()) == 20
    assert len(group2.all_results_of_prediction_races()) == 10


def test_runner_best_results_on_10_km_before_prediction_race(db):
    runner = RunnerFactory()
    race_result1 = HistoricalRaceResultFactory(
        runner=runner,
        time_result="0:49:00",
        historical_race=HistoricalRaceFactory(distance=10, start_date="2019-10-11"),
    )
    race_result2 = HistoricalRaceResultFactory(
        runner=runner,
        time_result="0:53:00",
        historical_race=HistoricalRaceFactory(distance=10, start_date="2019-09-11"),
    )
    race_result3 = HistoricalRaceResultFactory(
        runner=runner,
        time_result="0:52:00",
        historical_race=HistoricalRaceFactory(distance=10, start_date="2019-08-11"),
    )
    prediction_race = PredictionRaceFactory(start_date="2019-09-12")
    pred_race_result = PredictionRaceResultFactory(
        runner=runner, prediction_race=prediction_race
    )
    best_query = pred_race_result.best_10km_run_before_prediction_race
    assert str(best_query) == "0:52:00"


def test_runners_with_best_count(db):
    prediction_race = PredictionRaceFactory(start_date="2019-09-12")
    loop_number = 10
    for i in range(0, loop_number):
        runner = RunnerFactory()
        race = HistoricalRaceFactory(distance=10, start_date="2019-09-11")
        HistoricalRaceResultFactory.create_batch(
            size=20, runner=runner, historical_race=race
        )
        PredictionRaceResultFactory(runner=runner, prediction_race=prediction_race)

        runner2 = RunnerFactory()
        race2 = HistoricalRaceFactory(distance=60, start_date="2019-09-11")
        HistoricalRaceResultFactory.create_batch(
            size=20, runner=runner, historical_race=race2
        )
        PredictionRaceResultFactory(runner=runner2, prediction_race=prediction_race)
    prediction_race.refresh_from_db()
    assert prediction_race.runners_with_best_count(distance=10) == loop_number
    assert prediction_race.runners_with_best_count(distance=60) == loop_number
    assert prediction_race.runners_with_best_count(distance=5) == 0


@pytest.mark.parametrize(
    "time_result, hours",
    [("00:30:00", "0.5"), ("00:06:00", "0.1"), ("01:30:00", "1.5"), ("00:00:00", "0")],
)
def test_time_result_in_hours(time_result, hours, db):
    pr = PredictionRaceResultFactory.create(time_result=time_result)
    pr.refresh_from_db()
    assert pr.time_result_in_hours == Decimal(hours)

def test_runner_age_during_race(db):
    runner = RunnerFactory(birth_year=1980)
    race = PredictionRaceFactory(start_date = "2019-11-11")
    result = PredictionRaceResultFactory(runner=runner, prediction_race=race)
    result.refresh_from_db()
    assert result.runner_age_during_race == 39


def test_month_of_the_race(db):
    race = PredictionRaceFactory(start_date="2019-12-11")
    race.refresh_from_db()
    assert race.month_of_the_race == "December"

