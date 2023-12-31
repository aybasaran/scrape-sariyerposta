from typing import List

from postgrest.exceptions import APIError
from slugify import slugify

from db.supabase import Supabase
from utils.helpers import (
    convertScrapedDatetimeTextToDatetime,
    dontLetFourSlashToBeInUrl,
    removeAssetUrlsFromSitemap,
    removeMainPagesFromSitemap,
)
from utils.logger import Logger
from utils.scraper import HtmlScraper, XMLScraper
from utils.types import LogType, Post

logger = Logger()


class SariyerPostaScraper:
    domain = "https://www.sariyerposta.com"
    supabase: Supabase = None

    def __init__(self, supabase: Supabase) -> None:
        self.supabase = supabase

    def getPostDetails(self, url: str) -> Post or None:
        if not url.startswith(self.domain):
            url = f"{self.domain}/{url}"

        doc = HtmlScraper(url).scrape()
        try:
            postHeader = doc.find("div", {"class": "post-header"})
            postTitle = postHeader.find("h1").text.strip()
            postDescription = postHeader.find("h2").text.strip()
            postCategory = (
                postHeader.find("div", {"class": "meta-category"}).findAll("a")[1].attrs["href"].replace("/", "")
            )
            postPublishDate = postHeader.findAll("div", {"class": "box"})[0].findAll("span")[0].text.strip()
            postBodyElement = doc.find("div", {"class": "article-text"})
            postImage = doc.find("div", {"class": "news-section"}).findAll("img")[0].attrs["src"]
        except Exception as e:
            logger.log(LogType.ERROR, f"Error while scraping post: {url}")
            return None

        postContent = []

        for tag in postBodyElement.find_all(["p", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"]):
            if tag.name == "p":
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
            "category": postCategory,
            "created_at": convertScrapedDatetimeTextToDatetime(postPublishDate),
            "image": postImage,
            "content": postContent,
        }

    def getMontlySitemap(self) -> List[str]:
        doc = XMLScraper(f"{self.domain}/sitemap.xml").scrape()
        return [loc.text for loc in doc.findAll("loc")[1:]]

    def getMonthlyPosts(self) -> List[str]:
        postUrls = []
        monthlySitemapList = self.getMontlySitemap()

        for i, sitemap in enumerate(monthlySitemapList):
            doc = XMLScraper(sitemap).scrape()
            for j, loc in enumerate(
                filter(
                    dontLetFourSlashToBeInUrl,
                    filter(
                        removeMainPagesFromSitemap,
                        filter(
                            removeAssetUrlsFromSitemap,
                            doc.findAll("loc"),
                        ),
                    ),
                ),
            ):
                # Last Month's Urls includes main page so we need to skip it
                if i == 0 and j == 0:
                    continue
                postUrls.append(loc.text)

        return postUrls

    def scrapeAndSaveSingleNews(self, url: str):
        if not url.startswith(self.domain):
            url = f"{self.domain}/{url}"

        post = self.getPostDetails(url)
        self.supabase.saveNews(post)
        print(f"News {post['title']} saved to database.")

    def startScraping(self) -> None:
        logger.log(LogType.WARNING, "Scraping started...")
        postUrls = self.getMonthlyPosts()

        for url in postUrls:
            try:
                logger.log(LogType.INFO, f"Scraping {url}...")
                post = self.getPostDetails(url)
                if post:
                    self.supabase.saveNews(post)
                    logger.log(LogType.SUCCESS, f"Post {post['title']} saved to database.")
                else:
                    logger.log(LogType.ERROR, f"Post {url} couldn't be saved to database.")
            except Exception as e:
                continue
