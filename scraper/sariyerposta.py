from datetime import datetime

from slugify import slugify

from db.supabase import Supabase
from utils.helpers import removeAssetUrlsFromSitemap, removeMainPagesFromSitemap
from utils.scraper import HtmlScraper, XMLScraper


class SariyerPostaScraper:
    domain = "https://www.sariyerposta.com"
    supabase: Supabase = None

    def __init__(self, supabase: Supabase) -> None:
        self.supabase = supabase
        self.supabase.connect()

    def getNewsDetails(self, url: str):
        if not url.startswith(self.domain):
            url = f"{self.domain}/{url}"

        doc = HtmlScraper(url).scrape()

        postHeader = doc.find("div", {"class": "post-header"})
        postTitle = postHeader.find("h1").text
        postDescription = postHeader.find("h2").text
        postSubject = postHeader.find("div", {"class": "meta-category"}).findAll("a")[1].attrs["href"].replace("/", "")
        postPublishDate = postHeader.findAll("div", {"class": "box"})[0].findAll("span")[0].text
        postBodyElement = doc.find("div", {"class": "article-text"})
        postImage = doc.find("div", {"class": "news-section"}).findAll("img")[0].attrs["src"]

        postContent = []

        for tag in postBodyElement.find_all(["p", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"]):
            if tag.name == "p" and tag.text != "" and len(tag.text) > 10:
                if tag.find("img"):
                    postContent.append({"type": "image", "body": tag.find("img").attrs["src"]})
                else:
                    postContent.append({"type": "paragraph", "body": tag.text})
            elif tag.name == "ul" or tag.name == "ol":
                postContent.append({"type": "list", "body": [li.text for li in tag.find_all("li")]})
            elif tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                postContent.append({"type": "header", "body": tag.text})

        return {
            "title": postTitle,
            "slug": slugify(postTitle),
            "description": postDescription,
            "subject": postSubject,
            "publish_date": postPublishDate,
            "image": postImage,
            "content": postContent,
        }

    def getMontlySitemap(self):
        doc = XMLScraper(f"{self.domain}/sitemap.xml").scrape()
        return [loc.text for loc in doc.findAll("loc")[1:]]

    def getMonthlyNews(self):
        newsUrls = []
        monthlySitemapList = self.getMontlySitemap()

        for i, sitemap in enumerate(monthlySitemapList):
            doc = XMLScraper(sitemap).scrape()
            for j, loc in enumerate(
                filter(
                    removeMainPagesFromSitemap,
                    filter(
                        removeAssetUrlsFromSitemap,
                        doc.findAll("loc"),
                    ),
                )
            ):
                # Last Month's Urls includes main page so we need to skip it
                if i == 0 and j == 0:
                    continue
                newsUrls.append(loc.text)

        return newsUrls

    def startScraping(self):
        newsUrls = self.getMonthlyNews()
        for url in newsUrls:
            news = self.getNewsDetails(url)
            self.supabase.saveNews(news)
            break
