from config.config import Config
from db.supabase import Supabase

from scraper.sariyerposta import SariyerPostaScraper
from scraper.newspaper import NewsPaperScraper


if __name__ == "__main__":
    config = Config()
    supabase = Supabase(config)

    # newsPaperHeadlineScraper = NewsPaperScraper(supabase, config)
    # newsPaperHeadlineScraper.startScraping()

    scraper = SariyerPostaScraper(supabase, config)
    scraper.startScraping()
