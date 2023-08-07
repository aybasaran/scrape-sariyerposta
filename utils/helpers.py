# Remove asset urls from sitemap
from bs4 import PageElement

mainPages = [
    "/sariyer-haberleri",
    "/ekonomi",
    "/yasam",
    "/siyaset",
    "/roportaj",
    "/emlak",
    "/aktuel",
    "/alt-mansetler",
    "/saglik",
    "/kose-yazilari-arsiv",
    "/kose-yazilari",
    "/kultur-sanat",
    "/teknoloji",
    "/spor",
    "/egitim",
    "/foto-galeri",
    "/guncel-haberler",
    "/magazin",
    "/turkiye-ve-dunya-gundemi ",
    "/video-galeri",
    "/son-dakika-haberi",
    "/gundem",
    "/sektor",
]


def removeAssetUrlsFromSitemap(sitemapUrlElemet: PageElement):
    if (
        sitemapUrlElemet.text.endswith(".png")
        or sitemapUrlElemet.text.endswith(".jpg")
        or sitemapUrlElemet.text.endswith(".jpeg")
        or sitemapUrlElemet.text.endswith(".webp")
        or sitemapUrlElemet.text.endswith(".JPG")
        or sitemapUrlElemet.text.endswith(".PNG")
        or sitemapUrlElemet.text.endswith(".JPEG")
        or sitemapUrlElemet.text.endswith(".WEBP")
    ):
        return False
    return True


def removeMainPagesFromSitemap(sitemapUrlElemet: PageElement):
    # check if url is in main pages
    for mainPage in mainPages:
        if mainPage in sitemapUrlElemet.text:
            return False
    return True
