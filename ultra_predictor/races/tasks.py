import logging
from celery import chain, group, chord
from config import celery_app
from .models import PredictionRace
from .extras.itra_result_fetcher import ItraRaceResultFetcher
from .extras.itra_runner_birth_fetcher import ItraRunnerBirthFetcher
from .extras.itra_result_parser import ItraRaceResultsParser, ItraRunnerProfileParser
from .models import PredictionRaceResult, Runner


logger = logging.getLogger(__name__)


@celery_app.task
def process_itra_download(race_id):
    """First task download results from itra page with one shot
       then every result fire new task to download year of birth.
    """
    chain_process = chain(
        fetch_result_data_from_itra.s(race_id), group_itra_year_fetcher_task.s()
    )
    return chain_process


@celery_app.task()
def group_itra_year_fetcher_task(results):
    # return chord(fetch_year_and_save_results.s(result) for result in results)(
    #     finisher.s()
    # )#43397
    return group(fetch_year_and_save_results.s(result) for result in results)()


@celery_app.task()
def fetch_result_data_from_itra(race_id):
    """Download  race results from itra page"""
    itra_fetcher = ItraRaceResultFetcher(itra_race_id=race_id)
    itra_parser = ItraRaceResultsParser(itra_fetcher.get_data())
    return [result.to_dict() for result in itra_parser.race_results]


@celery_app.task()
def fetch_year_and_save_results(result):
    itra_birth = ItraRunnerBirthFetcher(
        first_name=result["first_name"], last_name=result["last_name"]
    )
    logger.error(result)
    itra_parser = ItraRunnerProfileParser(itra_birth.get_data())
    return itra_parser.birth_year
