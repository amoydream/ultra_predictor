import requests
from requests.exceptions import HTTPError


class ItraRaceResultFetcher:
    def __init__(self, itra_race_id):
        self.itra_race_id = itra_race_id

    def get_data(self):
        print("testin mock")
        try:
            headers = {"Accept-Language": "en-US,en;q=0.5"}
            response = requests.post(
                "https://itra.run/fiche.php",
                data={"mode": "getCourse", "idedition": self.itra_race_id},
                headers=headers,
            )

            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            return response.text

