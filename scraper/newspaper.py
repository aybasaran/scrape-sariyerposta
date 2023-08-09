import time
from datetime import datetime
from typing import List

from postgrest.exceptions import APIError
from storage3.utils import StorageException

from config.config import Config
from db.supabase import Supabase
from utils.scraper import HtmlScraper
from utils.types import NewsPaperHeadLine


class NewsPaperScraper:
    domain: str = "https://www.cumhuriyet.com.tr"
    supabase: Supabase = None
    config: Config = None

    def __init__(self, supabase: Supabase, config: Config) -> None:
        self.supabase = supabase
        self.config = config

    def getNewsPaperHeadlines(self) -> List[NewsPaperHeadLine]:
        headLines: List[NewsPaperHeadLine] = []
        doc = HtmlScraper(f"{self.domain}/gazete_mansetleri").scrape()

        headLineWrapperElements = doc.findAll("div", {"class": "gazete-manset"})

        for headLineWrapperElement in headLineWrapperElements:
            headLineEl = headLineWrapperElement.find("div", {"class": "gazete"})
            headLineImgEl = headLineEl.find("img")
            headLines.append(
                {
                    "newspaper_name": str.lower(headLineImgEl.attrs["alt"]),
                    "image": f"{self.domain}{headLineImgEl.attrs['src']}",
                    "created_at": datetime.now().isoformat(),
                }
            )

        return headLines

    def startScraping(self) -> None:
        print("Scraping NewsPaper Headlines...")

        headlines = self.getNewsPaperHeadlines()

        for headline in headlines:
            try:
                self.supabase.saveNewsPaperHeadline(headline)
            except Exception as e:
                if isinstance(e, APIError):
                    print(e.args[0]["message"])
                    continue
            finally:
                time.sleep(1)
                print(f"Saved {headline['newspaper_name']} headline")

        print("Scraping NewsPaper Headlines Completed")
