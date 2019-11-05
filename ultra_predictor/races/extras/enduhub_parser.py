from bs4 import BeautifulSoup
from decimal import Decimal
import re


class EnduhubParser:
    def __init__(self, html, birth_year_filter):
        self.html = html
        self.birth_year_filter = birth_year_filter
        self.soup = BeautifulSoup(html, "html.parser")
        self.has_next_page = self.check_next_page()

    def results(self):
        race_results = []
        for row in self.soup.find_all("tr", class_="Zawody"):
            runner_name = row.find("td", class_="name").get_text().strip()
            race_name = row.find("td", class_="event").get_text().strip()
            distance = row.find("td", class_="distance").get_text()
            start_date = row.find("td", class_="date").get_text()
            birth_year = row.find("td", class_="yob").get_text()
            time_result = row.find("td", class_="best").get_text()
            race_type = row.find("td", class_="sport").get_text()

            race_result = dict(
                runner_name=" ".join(runner_name.split()),
                birth_year=birth_year,
                race_name=" ".join(race_name.split()),
                distance=DistanceConverter(distance).distance_in_km,
                start_date=start_date,
                time_result=time_result,
                race_type=RaceTypeConverter(race_type).short_string,
            )
            try:
                equal_year = self.birth_year_filter == BirthYear(birth_year)
            except ValueError:
                continue
            else:
                if (
                    equal_year
                    and race_result["distance"]
                    and race_result["race_type"]
                    and len(race_result["time_result"].split(":")) == 3
                ):
                    race_results.append(race_result)
        return race_results

    def check_next_page(self):
        try:
            next_li = self.soup.select(".pagination .pages li.active")[0].findNext("li")
        except IndexError:
            return False
        else:
            return "ostatnia" not in next_li.text


class BirthYear:
    def __init__(self, year):
        if not str(year).isnumeric():
            raise ValueError("Birth year has to be a number")
        self.year = year

    @property
    def year(self):
        return int(self._year)

    @year.setter
    def year(self, y):
        self._year = y
        if len(str(y)) == 2:
            self._year = int(y) + 1900

    def __str__(self):
        return str(self.year)

    def __eq__(self, other):
        return self.year == other

    def __repr__(self):
        return f"BirthYear({self.year})"


class DistanceConverter:
    def __init__(self, distance_input):
        self.distance_input = distance_input
        self.distance_in_km = None
        self.correct_distance()

    def correct_distance(self):
        """Clean distance input"""
        str_distance = str(self.distance_input).strip()
        find_digit = re.match(r"\d+\.*\d*", str_distance)
        if find_digit:
            result = find_digit.group()
            self.distance_in_km = str(Decimal(result))

        elif str_distance.lower() == "maraton":
            self.distance_in_km = str(42.1)
        elif str_distance.lower() in ["połmaraton", "polmaraton", "półmaraton"]:
            self.distance_in_km = str(21.05)


class RaceTypeConverter:
    def __init__(self, race_type_input):
        self.race_type_input = race_type_input
        self.short_string = self.correct_race_type()

    def correct_race_type(self):
        if self.race_type_input == "Bieganie":
            return "f"
        if self.race_type_input == "Biegi Górskie":
            return "m"
        return None
