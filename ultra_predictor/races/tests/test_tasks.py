import pytest
from celery.result import EagerResult
from celery import chain
from .factories import PredictionRaceFactory
from ..tasks import process_itra_download


@pytest.mark.django_db
def test_task_fetch_result_data_from_itra(settings):
    """A basic test to execute the get_users_count Celery task."""
    prediction_race = PredictionRaceFactory()
    settings.CELERY_TASK_ALWAYS_EAGER = True
    #task = process_itra_download(prediction_race.id)
    task = process_itra_download(43397)
    task.delay()
    #assert task.get() == "OK"
    prediction_race.refresh_from_db()
    #assert prediction_race.prediction_race_results.count() == len(task.result)
