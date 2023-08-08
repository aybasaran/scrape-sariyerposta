from db.supabase import Supabase
from scraper.sariyerposta import SariyerPostaScraper

if __name__ == "__main__":
    supabase = Supabase()
    scraper = SariyerPostaScraper(supabase)
    scraper.startScraping()
