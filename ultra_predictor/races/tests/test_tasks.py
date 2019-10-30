from unittest.mock import patch
import pytest
from celery.result import EagerResult
from celery import chain
from .factories import PredictionRaceFactory, RunnerFactory
from ..tasks import process_itra_download, process_enduhub_download
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


def test_task_enduhub_fecher(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    runner = RunnerFactory()
    task = process_enduhub_download(runner.id)
    task.delay()
