from bs4 import PageElement
from datetime import datetime

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
    return datetime.strptime(scrapedDatetimeText, "%d.%m.%Y - %H:%M").strftime("%Y-%m-%d %H:%M:%S")
