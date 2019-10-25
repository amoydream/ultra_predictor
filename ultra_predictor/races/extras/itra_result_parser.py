from bs4 import BeautifulSoup
from .func import itra_name_extractor


class ItraRaceResultsParser:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")
        self.race_results = self.__parse_race_results()
        try:
            self.race_name = self.soup.h2.text
        except AttributeError:
            raise ValueError("Wrong HTML: there is no h2 header")

    def __parse_race_results(self):
        rows = self.soup.select("tbody tr")
        itra_race_results = []
        for row in rows:
            itra_race_results.append(ItraRaceResult(row))
        return itra_race_results
    
    
    

class ItraRaceResult:
    def __init__(self, row=None):

        extracted_name = itra_name_extractor(row.select("td")[0].text)
        self.first_name = extracted_name["first_name"].title()
        self.last_name = extracted_name["last_name"].title()
        self.time_result = row.select("td")[1].text.strip()
        self.position = row.select("td")[2].text
        self.sex = row.select("td")[3].text[:1]
        self.nationality = row.select("td")[4].text

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "time_result": self.time_result,
            "position": self.position,
            "sex": self.sex,
            "nationality": self.nationality,
        }

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.time_result}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name} {self.time_result}"


class ItraRunnerProfileParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.birth_year = self.soup.select(".tit")[0].text[-4:]
