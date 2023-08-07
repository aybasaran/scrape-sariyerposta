from utils.scraper import HtmlScraper, XMLScraper
from utils.helpers import removeAssetUrlsFromSitemap, removeMainPagesFromSitemap


class SariyerPostaScraper:
    domain = "https://www.sariyerposta.com"

    def getNewsDetails(self, url: str):
        doc = HtmlScraper(url).scrape()

        postHeader = doc.find("div", {"class": "post-header"})
        postTitle = postHeader.find("h1").text
        postDescription = postHeader.find("h2").text
        postSubject = postHeader.find("div", {"class": "meta-category"}).findAll("a")[1].attrs["href"]

        print(postTitle)
        print(postDescription)
        print(postSubject)

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
        count = 0
        newsUrls = self.getMonthlyNews()
        for url in newsUrls:
            self.getNewsDetails(url)
            count += 1
            if count == 3:
                break
