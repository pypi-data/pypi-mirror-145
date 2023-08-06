import requests
from bs4 import BeautifulSoup
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Search:

    def __init__(self):
        self.google_search = "https://google.com/search?q="
        self.sites = ["stackoverflow.com"]
        self.parsed_results = []

    def search(self, query):

        results = self.get(query=query)

        self.parseResults(results=results)

        if len(self.parsed_results) > 0:

            reversed_results = list(reversed(self.parsed_results))

            for res in reversed_results:

                print(res['name'])
                print(res['url'])
                print(res['divider'])

        else:
            print(bcolors.WARNING + "No results found.")

        self.parsed_results.clear()

    def searchAndOpen(self, query, result):

        results = self.get(query)

        self.parseResults(results=results)

        if len(self.parsed_results) > 0 and result < len(self.parsed_results):

            os.system(
                f'python -m webbrowser https://{self.sites[0]}/questions/{self.parsed_results[result]["url"].split("/")[-2]}')

        print(bcolors.OKGREEN + f"Opened {self.parsed_results[result]['url']}")

    def get(self, query):

        if len(self.sites) == 1:

            url = self.google_search + \
                query.replace(" ", "+")+f"+site:{self.sites[0]}"

            response = requests.get(url)

        return response

    def parseResults(self, results):

        if len(self.sites) == 1:

            soup = BeautifulSoup(results.text, 'html.parser')

            for result in soup.find_all('a'):

                if f'{self.sites[0]}/questions' in result['href']:

                    self.parsed_results.append({
                        "name": bcolors.OKGREEN + " ".join(result['href'].split('/')
                                                           [-1].split('&')[0].split("-")).title() + bcolors.BOLD,
                        "url": bcolors.OKBLUE + result['href'].replace("/url?q=", ''),
                        "divider": bcolors.WARNING + '--------------------------------------'
                    })
