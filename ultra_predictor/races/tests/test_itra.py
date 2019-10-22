import pytest

from ..extras.itra_parser import ItraRaceResultsParser, ItraRaceResult


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
    assert race_result.runner_name == "Bartlomiej Przedwojewski"


