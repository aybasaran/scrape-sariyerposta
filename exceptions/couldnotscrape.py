class CouldNotScrape(Exception):
    def __init__(
        self,
    ) -> None:
        self.message = "Could not scrape the page"
        super().__init__(self.message)
