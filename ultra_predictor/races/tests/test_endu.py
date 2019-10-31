from unittest.mock import patch
import pytest
from ..extras.enduhub_parser import (
    EnduhubParser,
    BirthYear,
    DistanceConverter,
    RaceTypeConverter,
)
from ..extras.enduhub_fetcher import EnduhubFetcher


def testing_initialization_of_enduhub_parser(eduhub_page_html_1):
    birth_year_filter = 1980
    endu_parser = EnduhubParser(eduhub_page_html_1, birth_year_filter)
    assert endu_parser.html == eduhub_page_html_1
    assert endu_parser.birth_year_filter == birth_year_filter


def test_results(eduhub_page_html_1):
    """Test results that return  filtered results year"""
    birth_year_filter = 1987
    endu_parser = EnduhubParser(eduhub_page_html_1, birth_year_filter)
    assert len(endu_parser.results()) == 3


def test_birth_year_init():
    birth = BirthYear(1980)
    assert str(birth) == "1980"
    assert birth.year == 1980


def test_birth_year_init_short():
    birth = BirthYear(80)
    assert str(birth) == "1980"
    assert birth.year == 1980


@pytest.mark.parametrize(
    "year, year_to_birth", [(1980, 80), (1980, "80"), (1980, "1980")]
)
def test_birth_year_equl(year, year_to_birth):
    assert year == BirthYear(year_to_birth)


def test_birth_year_non_numerical():
    with pytest.raises(ValueError):
        BirthYear("asd")


@pytest.mark.parametrize(
    "dinstance_input, distance_output",
    [("10", "10"), ("17 km", "17"), ("maraton", "42.1")],
)
def test_distance_converter(dinstance_input, distance_output):
    distance = DistanceConverter(dinstance_input)
    assert distance.distance_in_km == distance_output


@pytest.mark.parametrize(
    "race_type_input, race_type_output",
    [("Biegi Górskie", "m"), ("Bieganie", "f"), ("anything else", None)],
)
def test_race_type_converter(race_type_input, race_type_output):
    race_type_converted = RaceTypeConverter(race_type_input)
    assert race_type_converted.short_string == race_type_output


@patch("ultra_predictor.races.extras.enduhub_fetcher.EnduhubFetcher.get_data")
@patch("ultra_predictor.races.extras.enduhub_parser.EnduhubParser.check_next_page")
def test_endu_case(patch_check_next_page, patch_download_endu, eduhub_page_html_1):
    patch_download_endu.return_value = eduhub_page_html_1
    patch_check_next_page.return_value = False
    page = 1
    all_results = []

    while True:
        endu_fetcher = EnduhubFetcher("Piotr Nowak", page)
        endu_parser = EnduhubParser(endu_fetcher.get_data(), 1987)
        all_results += endu_parser.results()
        if endu_parser.has_next_page:
            page += 1
        else:
            break
    # endu_fetcher.get_data = mock.Mock()
    # endu_fetcher.get_data.return_value = itra_html
    assert len(all_results) == 3
