import requests
from bs4 import BeautifulSoup
from exceptions.couldnotscrape import PageLoadFailed


class SariyerPostaScraper:
    domain = "https://www.sariyerposta.com"

    def getNewsDetails(self, route: str):
        response = requests.get(self.domain + "/" + route)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            postHeader = soup.find("div", {"class": "post-header"})
            postTitle = postHeader.find("h1").text
            postDescription = postHeader.find("h2").text
            postSubject = (
                postHeader.find("div", {"class": "meta-category"})
                .findAll("a")[1]
                .attrs["href"]
            )

            print(postTitle)
            print(postDescription)
            print(postSubject)

            response.close()
            response = None

        else:
            raise PageLoadFailed()

    def newsListFromSiteMap(self):
        pass
