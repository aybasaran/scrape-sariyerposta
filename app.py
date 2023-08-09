from db.supabase import Supabase
from scraper.sariyerposta import SariyerPostaScraper
from config.config import Config

if __name__ == "__main__":
    Config().load()
    supabase = Supabase()
    scraper = SariyerPostaScraper(supabase)
    scraper.startScraping()
