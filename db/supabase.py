from io import BytesIO

import requests
from PIL import Image
from supabase import Client, create_client

from config.config import Config
from exceptions.db import CouldNotConnectDB
from utils.types import NewsPaperHeadLine, LogType
from utils.logger import Logger

logger = Logger()


class Supabase:
    client: Client = None
    config: Config = None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.connect()

    def connect(self) -> None:
        try:
            supabase: Client = create_client(self.config.SUPABASE_URL, self.config.SUPABASE_KEY)
            self.client = supabase
        except Exception as e:
            raise CouldNotConnectDB()

    def saveNewsPaperHeadline(self, headline: NewsPaperHeadLine) -> None:
        # First Upload Images to Supabase Storage
        headline["image"] = self.uploadImage(headline["image"], folder="headline")

        self.client.table("headline").insert(
            {
                "newspaper_name": headline["newspaper_name"],
                "image": headline["image"],
                "created_at": headline["created_at"],
            }
        ).execute()

    def saveNews(self, post: dict) -> None:
        # check if post already exists
        if self.client.table("post").select("*").eq("slug", post["slug"]).execute().count:
            logger.log(LogType.INFO, f"Post already exists: {post['slug']}")
            return

        # Upload Main Image to Supabase Storage
        image = self.uploadImage(post["image"], folder="post")

        # Upload Content images to Supabase Storage
        for content in post["content"]:
            if content["type"] == "image":
                content["body"] = self.uploadImage(content["body"], folder="post")

        self.client.table("post").insert(
            {
                "title": post["title"],
                "slug": post["slug"],
                "description": post["description"],
                "created_at": post["created_at"],
                "image": image,
                "category": post["category"],
                "content": post["content"],
            }
        ).execute()

    def uploadImage(self, image: str, folder: str) -> str:
        img_name = image.split("/")[-1].split(".")[0]

        r = requests.get(image, stream=True)

        if r.status_code != 200:
            raise Exception("Could not download image")

        # Convert image to webp
        img = Image.open(BytesIO(r.content))
        b = BytesIO()
        img.save(b, format="webp", optimize=True)

        response = self.client.storage.from_(self.config.SUPABASE_BUCKET).upload(
            folder + "/" + img_name + ".webp", b.getvalue(), {"content-type": "image/webp"}
        )

        if response.status_code == 200:
            public_url = (
                f"{self.config.SUPABASE_URL}/storage/v1/object/public/{self.config.SUPABASE_BUCKET}/{folder}/"
                + img_name
                + ".webp"
            )

            return public_url

        return None
