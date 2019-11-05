import requests
from requests.exceptions import HTTPError


class ItraRunnerBirthFetcher:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_data(self):
        print("testin mock", self.first_name, self.last_name)
        try:
            headers = {"Accept-Language": "en-US,en;q=0.5"}
            response = requests.post(
                "https://itra.run/fiche.php",
                data={"mode": "search", "pnom": self.first_name, "nom": self.last_name},
                headers=headers,
            )

            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            return response.text

   