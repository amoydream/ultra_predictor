import requests
from requests.exceptions import HTTPError


class EnduhubFetcher:
    def __init__(self, runner_name, page):
        self.runner_name = runner_name
        self.page = page

    def get_data(self):
        try:
            link_template = "https://enduhub.com/pl/search/?name={}&page={}"
            link = link_template.format(self.runner_name, self.page)
            print(link)
            response = requests.get(link)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            return response.text

