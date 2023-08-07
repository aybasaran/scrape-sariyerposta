class CouldNotConnectDB(Exception):
    def __init__(
        self,
    ) -> None:
        self.message = "Could not connect to the database"
        super().__init__(self.message)
