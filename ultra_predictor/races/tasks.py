import logging
from celery import chain, group, chord
from config import celery_app
from django.db import transaction
from .models import PredictionRace
from .extras.itra_result_fetcher import ItraRaceResultFetcher
from .extras.itra_runner_birth_fetcher import ItraRunnerBirthFetcher
from .extras.itra_result_parser import ItraRaceResultsParser, ItraRunnerProfileParser
from .extras.enduhub_fetcher import EnduhubFetcher
from .extras.enduhub_parser import EnduhubParser
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
    return group(
        fetch_year_and_save_results.s(result, results["race_id"])
        for result in results["results"]
    )()


@celery_app.task(bind=True, default_retry_delay=60, max_retries=120)
def fetch_result_data_from_itra(self, race_id):
    """Download  race results from itra page"""
    itra_fetcher = ItraRaceResultFetcher(itra_race_id=race_id)
    itra_parser = ItraRaceResultsParser(itra_fetcher.get_data())
    return {
        "results": [result.to_dict() for result in itra_parser.race_results],
        "race_id": race_id,
    }


@celery_app.task(bind=True, default_retry_delay=60, max_retries=120)
def fetch_year_and_save_results(self, result, race_id):
    """Find year on Itra Page and save runner and race results"""
    
    prediction_race = PredictionRace.objects.get(pk=race_id)
    itra_birth = ItraRunnerBirthFetcher(
        first_name=result["first_name"], last_name=result["last_name"]
    )
    itra_parser = ItraRunnerProfileParser(itra_birth.get_data())
    with transaction.atomic():
        runner, created = Runner.objects.get_or_create(
            first_name=result["first_name"],
            last_name=result["last_name"],
            sex=result["sex"],
            nationality=result["nationality"],
            birth_year=itra_parser.birth_year,
        )
        result, created = PredictionRaceResult.objects.get_or_create(
            runner=runner,
            prediction_race=prediction_race,
            time_result=result["time_result"],
            position=result["position"],
        )
    return itra_parser.birth_year


@celery_app.task(bind=True, default_retry_delay=60, max_retries=120)
def process_enduhub_download(self, runner_id):
    runner = Runner.objects.get(pk=runner_id)
    page = 1
    all_results = []
    while True:
        endu_fetcher = EnduhubFetcher(runner.name, page)
        endu_parser = EnduhubParser(endu_fetcher.get_data(), runner.birth_year)
        all_results += endu_parser.results()

        if endu_parser.has_next_page:
            page += 1
        else:
            break

    return all_results        