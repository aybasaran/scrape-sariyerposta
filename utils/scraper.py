import requests
from bs4 import BeautifulSoup
from exceptions.couldnotscrape import CouldNotScrape


class HtmlScraper:
    def __init__(self, url) -> None:
        self.url = url

    def scrape(self) -> BeautifulSoup:
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, "html.parser")

            return soup
        except Exception as e:
            raise CouldNotScrape()
        finally:
            response.close()
            response = None


class XMLScraper:
    def __init__(self, url) -> None:
        self.url = url

    def scrape(self) -> BeautifulSoup:
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, features="xml")

            return soup
        except Exception as e:
            raise CouldNotScrape()
        finally:
            response.close()
            response = None
