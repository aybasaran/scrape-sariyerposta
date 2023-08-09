from dotenv import load_dotenv
from exceptions.config import CouldNotLoadConfig

import os


class Config:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""
    SUPABASE_BUCKET = ""

    def load(self) -> None:
        try:
            load_dotenv()
            self.SUPABASE_URL = os.environ.get("SUPABASE_URL")
            self.SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
            self.SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")
        except Exception as e:
            raise CouldNotLoadConfig()
