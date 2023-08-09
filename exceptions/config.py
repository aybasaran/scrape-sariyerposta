class CouldNotLoadConfig(Exception):
    def __init__(
        self,
    ) -> None:
        self.message = "Could not load the environment variables"
        super().__init__(self.message)
