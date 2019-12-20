import scrapy
import logging
from bs4 import BeautifulSoup
import re
from dateutil import parser
from datetime import timedelta
from itra.items import Event, Race, RaceResult

logger = logging.getLogger()

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
}


class ItraSpider(scrapy.Spider):
    name = "itra"

    def start_requests(self):
        urls = []
        year = 2018
        for ids in range(1, 1000):
        #for ids in [639]:
            urls.append(
                (
                    f"https://itra.run/calend.php?id={ids}",
                    f"mode=getEvt&id={ids}&annee={year}",
                )
            )

        for url, body in urls:
            yield scrapy.Request(
                url=url,
                method="POST",
                headers=HEADERS,
                body=body,
                callback=self.parse_event,
                meta={"year": year, "itra_event_id": ids},
            )

    def parse_event(self, response):
        logger.info("----Start parsing EVENT------")
        itra_event_id = response.meta.get("itra_event_id")
        event_year = response.meta.get("year")
        soup = BeautifulSoup(response.body, "html.parser")
        event_name = (
            soup.select("#calevt_titre")[0].get_text("|").split("|")[-1].strip()
        )

        if event_name:
            logger.info(f"Found on page: {response.url}")

            func_click_to_parse = [
                a.get("onclick") for a in soup.select("#calevt_lst a")
            ]
            races = [
                func.replace("'", "").split("(")[-1].split(")")[0].split(",")
                for func in func_click_to_parse
            ]
            try:
                itra_id_found = races[0][0]
            except IndexError:
                itra_id_found = None
              
            if itra_id_found:
                event = Event(name=event_name, itra_id=int(races[0][0]), year=event_year)
                logger.info(f"Found Event: {event}")
                yield event
                for race in races:
                    event_id, year, race_id = [int(d) for d in race]

                    url, body = (
                        f"https://itra.run/calend.php?id={event_id}",
                        f"mode=getEvt&id={event_id}&annee={year}&idc={race_id}&opendirect=1",
                    )

                    yield scrapy.Request(
                        url=url,
                        method="POST",
                        headers=HEADERS,
                        body=body,
                        callback=self.parse_race,
                        meta={"itra_event_id": event_id, "itra_race_id": race_id},
                    )

    def parse_race(self, response):
        logger.info("----Start parsing RACE------")
        itra_event_id = response.meta.get("itra_event_id")
        itra_race_id = response.meta.get("itra_race_id")

        soup = BeautifulSoup(response.body, "html.parser")
        race_name = [
            t.strip()
            for t in soup.select("#race-container h2")[0].get_text("|").split("|")
        ][-1]

        icons = [
            icon.get("class")[1] for icon in soup.select("#race-container h2 .iconBig")
        ]
        itra_point, mount_point, finish_point = None, None, None
        for icon in icons:
            if icon.startswith("pts"):
                itra_point = re.search("\d+", icon)[0]
            if icon.startswith("mont"):
                mount_point = re.search("\d+", icon)[0]
            if icon.startswith("finish"):
                finish_point = soup.select(f".{icon}")[0].get_text()
        try:
            map_link = soup.select("iframe")[0].get("src")
        except IndexError:
            map_link = None
        participation = (
            soup.find_all(text=re.compile("Participation"))[0]
            .parent.findNext("td")
            .getText()
        )
        try:
            
            sentiers, pistes, routes = [
                re.search("\d+", r)[0]
                for r in soup.find_all(text=re.compile("% routes"))[0].split("/")
            ]
        except IndexError:
            sentiers, pistes, routes = None, None, None

        challenge = (
            soup.find('table').find_all(text=re.compile("Challenge"))[0]
            .parent.findNext("td")
            .getText()
        )
        championship = (
            soup.find('table').find_all(text=re.compile("Championship"))[0]
            .parent.findNext("td")
            .getText()
        )
        race_date_html = (
            soup.find('table').find_all(text=re.compile("Date and time of start"))[0]
            .parent.findNext("td")
            .getText()
        )
        race_date_parsed = parser.parse(race_date_html)
        race_date, race_time = str(race_date_parsed).split()

        location_start = (
            soup.find('table').find_all(text=re.compile("Location of start"))[0]
            .parent.findNext("td")
            .getText()
        )
        country_start = (
            re.search("\\(.*\)", location_start)[0].replace("(", "").replace(")", "")
        )
        city_start = location_start.split("(")[0].strip()

        location_finish = (
            soup.find('table').find_all(text=re.compile("Location of finish"))[0]
            .parent.findNext("td")
            .getText()
        )
        country_finish = (
            re.search("\\(.*\)", location_finish)[0].replace("(", "").replace(")", "")
        )
        city_finish = location_finish.split("(")[0].strip()

        distance = (
            soup.find('table').find_all(text=re.compile("Distance"))[0]
            .parent.findNext("td")
            .getText()
            .split("km")[0]
        )

        ascent = (
            soup.find('table').find_all(text=re.compile("Ascent"))[0]
            .parent.findNext("td")
            .getText()
            .split("m")[0]
        )
        
        descent = (
            soup.find('table').find_all(text=re.compile("Descent"))[0]
            .parent.findNext("td")
            .getText()
            .split("m")[0]
        )

        refreshment_points = (
            soup.find('table').find_all(text=re.compile("Refreshment points"))[0]
            .parent.findNext("td")
            .getText()
        )
        try:
            max_hour, max_minutes = [
                int(t)
                for t in soup.find_all(text=re.compile("Maximum time"))[0]
                .parent.findNext("td")
                .getText()
                .split(":")
            ]
            max_time = timedelta(hours=max_hour, minutes=max_minutes)
        except IndexError:
            max_time = None
            logger.info("Maximum Time not found")

        race = Race()
        race["name"] = race_name
        race["itra_event_id"] = itra_event_id
        race["itra_race_id"] = itra_race_id
        race["itra_point"] = itra_point
        race["mount_point"] = mount_point
        race["finish_point"] = finish_point
        race["map_link"] = map_link
        race["participation"] = participation
        race["sentiers"] = sentiers
        race["pistes"] = pistes
        race["routes"] = routes

        race["challenge"] = challenge
        race["championship"] = championship
        race["country_start"] = country_start
        race["city_start"] = city_start
        race["country_finish"] = country_finish
        race["city_finish"] = city_finish

        race["distance"] = distance
        race["race_date"] = race_date
        race["race_time"] = race_time
        race["ascent"] = ascent
        race["descent"] = descent
        race["refreshment_points"] = refreshment_points
        race["max_time"] = max_time

        yield race
        logger.info(f"Found race: {race}")

        # page = response.url.split("/")[-2]

        # date_to_send = parser.parse(race_date).strftime("%d/%m/%Y")

        # url, body = (
        #     f"https://itra.run/results.php",
        #     f"mode=getres&num_page=&input_cal_rech={race_name}&periode=perso&dtmin={date_to_send}&dtmax={date_to_send}",
        # )
        # yield scrapy.Request(
        #     url=url,
        #     method="POST",
        #     headers=HEADERS,
        #     body=body,
        #     callback=self.parce_find_race,
        # )

    def parce_find_race(self, response):
        logger.info("----Start search RACE for results------")
        soup = BeautifulSoup(response.body, "html.parser")
        race_id_results = re.search("\d+", soup.find("a").get("onclick"))[0]

        url, body = (
            f"https://itra.run/fiche.php",
            f"mode=getCourse&idedition={race_id_results}",
        )
        yield scrapy.Request(
            url=url,
            method="POST",
            headers=HEADERS,
            body=body,
            callback=self.parce_race_results,
        )
        # page = response.url.split("/")[-2]
        # filename = "found_race-%s.html" % page

        # with open(filename, "wb") as f:
        #     f.write(response.body)
        # self.log("Saved file %s" % filename)

    def parce_race_results(self, response):
        logger.info("----Start parcing results------")
        soup = BeautifulSoup(response.body, "html.parser")
        rows = soup.select("tbody tr")

        for row in rows:

            extracted_name = itra_name_extractor(row.select("td")[0].text)
            first_name = extracted_name["first_name"].title()
            last_name = extracted_name["last_name"].title()

            try:
                hours, minutes, seconds = [
                    int(t) for t in row.select("td")[1].text.strip().split(":")
                ]
                time_result = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except ValueError:
                time_result = "-"
            position = row.select("td")[2].text
            sex = row.select("td")[3].text[:1]
            nationality = row.select("td")[4].text
            result = RaceResult()
            result["first_name"] = first_name
            result["last_name"] = last_name
            result["time_result"] = time_result
            result["position"] = position
            result["sex"] = sex
            result["nationality"] = nationality
            yield result


def itra_name_extractor(name):
    """Extract name where last name is uppercase"""
    last_name = []
    first_name = []
    words = name.split(" ")
    for word in words:
        if word.isupper():
            last_name.append(word)
        else:
            first_name.append(word)

    return {"first_name": " ".join(first_name), "last_name": " ".join(last_name)}

