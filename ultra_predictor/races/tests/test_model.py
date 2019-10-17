from ultra_predictor.races.models import RaceGroup
def test_race_group_string():
    race_group = RaceGroup(name="Wielka Prehyba")
    assert str(race_group) == "Wielka Prehyba"