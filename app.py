from config.config import Config
from db.supabase import Supabase

from scraper.sariyerposta import SariyerPostaScraper
from scraper.newspaper import NewsPaperScraper


if __name__ == "__main__":
    config = Config()
    supabase = Supabase(config)

    newsPaperScraper = NewsPaperScraper(supabase)
    newsPaperScraper.startScraping()

    websiteScraper = SariyerPostaScraper(supabase)
    websiteScraper.startScraping()
