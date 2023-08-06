from argparse import Action
import requests
from bs4 import BeautifulSoup
import platform


class FetchAnswers(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))

        response = requests.get(
            f"https://google.com/search?q={values.replace(' ', '+')}+site:stackoverflow.com")

        soup = BeautifulSoup(response.text, 'html.parser')

        for aTag in soup.find_all('a'):

            if 'https://stackoverflow.com/' in aTag['href']:

                print(" ".join(aTag['href'].split('/')
                               [-1].split('&')[0].split("-")).title())
                print(aTag['href'].replace("/url?q=", ''))
                print('----------------------------------------------')

        setattr(namespace, self.dest, values)


print(platform.platform())
