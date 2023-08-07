from db.supabase import Supabase
from scraper.sariyerposta import SariyerPostaScraper

if __name__ == "__main__":
    supabase = Supabase().client
    scraper = SariyerPostaScraper()

    # routes = [
    #     "sariyerde-coken-istinat-duvari-buyuk-korku-yaratti",
    #     "sariyerde-sureklenen-tekne-kurtarildi",
    # ]

    # for route in routes:
    #     scraper.getNewsDetails(route)

    scraper.newsListFromSiteMap()
