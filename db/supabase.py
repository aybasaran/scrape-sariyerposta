import os

from supabase_py import Client, create_client


class Supabase:
    client: Client = None

    # init
    def __init__(self) -> None:
        self.connect()

    def connect(self):
        try:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")

            supabase: Client = create_client(url, key)
            self.client = supabase
        except Exception as e:
            raise Exception("Error while connecting to Supabase")
