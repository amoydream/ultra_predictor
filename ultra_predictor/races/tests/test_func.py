from ..extras.func import itra_name_extractor

def test_name_extractor_with_double_first_name():
    name = "Michał Jan MOJEK"
    extracted_name = itra_name_extractor(name)
    assert extracted_name["first_name"] == "Michał Jan"
    assert extracted_name["last_name"] == "MOJEK"

def test_name_extractor_with_double_last_name():
    name = "Michał BŁASZCZAK MOJEK"
    extracted_name = itra_name_extractor(name)
    assert extracted_name["first_name"] == "Michał"
    assert extracted_name["last_name"] == "BŁASZCZAK MOJEK"


def test_name_extractor_with_double_double():
    name = "Michał Jan BŁASZCZAK MOJEK"
    extracted_name = itra_name_extractor(name)
    assert extracted_name["first_name"] == "Michał Jan"
    assert extracted_name["last_name"] == "BŁASZCZAK MOJEK"
