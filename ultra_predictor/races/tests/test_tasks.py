from unittest.mock import patch
from os import path
import pytest
from celery.result import EagerResult
from celery import chain
from .factories import PredictionRaceFactory, RunnerFactory, PredictionRaceResultFactory
from ..tasks import (
    process_itra_download,
    fetch_enduhub_runner_download,
    process_endu_download,
    process_csv_files,
)
import shutil
from ..extras.itra_result_parser import ItraRaceResultsParser


@patch(
    "ultra_predictor.races.extras.itra_result_fetcher.ItraRaceResultFetcher.get_data"
)
@patch(
    "ultra_predictor.races.extras.itra_runner_birth_fetcher.ItraRunnerBirthFetcher.get_data"
)
@pytest.mark.django_db
def test_task_fetch_result_data_from_itra(
    patch_download_year_html,
    patch_download_race_results,
    settings,
    itra_runner_profile_html,
    itra_html,
):
    patch_download_year_html.return_value = itra_runner_profile_html
    patch_download_race_results.return_value = itra_html

    prediction_race = PredictionRaceFactory()
    settings.CELERY_TASK_ALWAYS_EAGER = True

    task = process_itra_download(prediction_race.id)
    task.delay()

    prediction_race.refresh_from_db()
    itra_parser = ItraRaceResultsParser(itra_html)
    assert prediction_race.prediction_race_results.count() == len(
        itra_parser.race_results
    )


@patch("ultra_predictor.races.extras.enduhub_fetcher.EnduhubFetcher.get_data")
@patch("ultra_predictor.races.extras.enduhub_parser.EnduhubParser.check_next_page")
@pytest.mark.django_db
def test_task_enduhub_fecher(
    patch_check_next_page, patch_endu_html, settings, eduhub_page_html_1
):
    patch_check_next_page.return_value = False
    patch_endu_html.return_value = eduhub_page_html_1
    settings.CELERY_TASK_ALWAYS_EAGER = True
    runner = RunnerFactory(first_name="Piotr", last_name="Nowak", birth_year="1987")
    task = fetch_enduhub_runner_download.delay(runner.id)
    assert runner.historical_race_results.count() == 3


@pytest.mark.django_db
def test_task_enduhub_process(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    result = PredictionRaceResultFactory()
    race = result.prediction_race
    process_endu_download.delay(race.id)


@pytest.mark.django_db
def test_task_process_csv_files(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.FOLDER_FOR_CSV = 'prediction_csv_test_task'
    result = PredictionRaceResultFactory()
    race = result.prediction_race
    group = race.prediction_race_group
    process_csv_files.delay(group.id)
    assert path.exists(
        f"{settings.FOLDER_FOR_CSV}/{settings.CSV_FILE_PREDICTION_GROUP_NAME_TEMPLATE}{group.id}.csv"
    )
    shutil.rmtree(settings.FOLDER_FOR_CSV)

