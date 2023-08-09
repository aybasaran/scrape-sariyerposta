from bs4 import PageElement
from datetime import datetime
import math
from utils.consts import mainPages, unWantedExtensions


def removeAssetUrlsFromSitemap(sitemapUrlElemet: PageElement):
    # check if url is in unwanted extensions
    for extension in unWantedExtensions:
        if extension in sitemapUrlElemet.text:
            return False
    return True


def removeMainPagesFromSitemap(sitemapUrlElemet: PageElement):
    # check if url is in main pages
    for mainPage in mainPages:
        if mainPage in sitemapUrlElemet.text:
            return False
    return True


def convertScrapedDatetimeTextToDatetime(scrapedDatetimeText: str):
    # remove spaces from scrapedDatetimeText
    scrapedDatetimeText = scrapedDatetimeText.replace(" ", "")
    # replace - with space
    scrapedDatetimeText = scrapedDatetimeText.replace("-", " ")

    return datetime.strptime(scrapedDatetimeText, "%d.%m.%Y %H:%M").isoformat()


def writeUrlsToFile(urls: list[str], fileName: str):
    with open(fileName, "w") as file:
        for url in urls:
            file.write(f"{url}\n")


def dontLetFourSlashToBeInUrl(urls: str):
    # https://www.sariyerposta.com.tr/subparam/slug === 4 slash
    # dont let slash count 3 to be in url
    for url in urls:
        if url.count("/") == 4:
            return False
        return True


def findUrlsStats(urls: list[str]) -> tuple[int, int, int]:
    total = 0
    min = 0
    max = 0
    # find min and max length of urls
    for url in urls:
        total += len(url)
        if min == 0 or len(url) < min:
            min = len(url)
        if max == 0 or len(url) > max:
            max = len(url)

    return min, max, math.floor(total / len(urls))
