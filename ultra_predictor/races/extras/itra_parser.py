from bs4 import BeautifulSoup


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
    def __init__(self, row):
        pass
