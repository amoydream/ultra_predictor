
from unittest import mock

import pytest
from ..extras.itra_result_parser import (
    ItraRaceResultsParser,
    ItraRaceResult,
    ItraRunnerProfileParser,
)
from ..extras.itra_result_fetcher import ItraRaceResultFetcher
from ..extras.itra_runner_birth_fetcher import ItraRunnerBirthFetcher


def test_loadind_file(itra_html):
    assert itra_html.startswith("<h2>Biegi W Szczawnicy 2019 - Wielka Prehyba</h2>")


def test_itra_parser_race_name(itra_html):
    """Test itra parser return correnct race name"""
    itra_parser = ItraRaceResultsParser(itra_html)
    assert itra_parser.race_name == "Biegi W Szczawnicy 2019 - Wielka Prehyba"


def test_itra_parser_error_race_html():
    """Test itra parser when html doesn't include header"""
    with pytest.raises(ValueError):
        ItraRaceResultsParser("<html></html>")


def test_itra_parser_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    assert len(itra_parser.race_results) == 16


def test_type_of_itra_parser_race_result_element(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    assert isinstance(race_result, ItraRaceResult)


def test_succes_parsing_of_runner_name_itra_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    assert race_result.first_name == "Bartlomiej"
    assert race_result.last_name == "Przedwojewski"


def test_succes_parsing_of_time_result_itra_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    assert race_result.time_result == "03:16:57"


def test_succes_parsing_of_postition_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    assert race_result.position == "1"


def test_succes_parsing_of_sex_itra_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    assert race_result.sex == "M"


def test_succes_parsing_of_nationality_itra_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    assert race_result.nationality == "Poland"


def test_succes_parsing_itra_year_of_runner(itra_runner_profile_html):
    itra_parser = ItraRunnerProfileParser(itra_runner_profile_html)
    assert itra_parser.birth_year == "1993"


def test_itra_result_asing_runner_birth_year(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    race_result.birth_year = "1985"
    assert race_result.birth_year == "1985"


def test_to_dict_race_results(itra_html):
    itra_parser = ItraRaceResultsParser(itra_html)
    race_result = itra_parser.race_results[0]
    race_result_dict = race_result.to_dict()
    assert race_result_dict["first_name"] == "Bartlomiej"
    assert race_result_dict["last_name"] == "Przedwojewski"
    assert race_result_dict["nationality"] == "Poland"
    assert race_result_dict["sex"] == "M"
    assert race_result_dict["position"] == "1"
    assert race_result_dict["time_result"] == "03:16:57"
    #assert race_result_dict["birth_year"] == "1985"


def test_itra_case(itra_html):
    itra_fetcher = ItraRaceResultFetcher(itra_race_id=43397)
    itra_fetcher.get_data = mock.Mock()
    itra_fetcher.get_data.return_value = itra_html
    itra_parser = ItraRaceResultsParser(itra_fetcher.get_data())
    race_result = itra_parser.race_results[0]
    assert race_result.first_name == "Bartlomiej"
    assert race_result.last_name == "Przedwojewski"
    assert race_result.nationality == "Poland"
    assert race_result.sex == "M"
    assert race_result.position == "1"
    assert race_result.time_result == "03:16:57"


def test_itra_runner_birth_fetcher(itra_runner_profile_html):
    itra_birth = ItraRunnerBirthFetcher(
        first_name="Bartlomiej", last_name="Przedwojewski"
    )
    itra_birth.get_data = mock.Mock()
    itra_birth.get_data.return_value = itra_runner_profile_html
    itra_parser = ItraRunnerProfileParser(itra_birth.get_data())
    assert itra_parser.birth_year == "1993"

