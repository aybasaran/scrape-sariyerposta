import os

from supabase import Client, create_client
from exceptions.db import CouldNotConnectDB

import requests
from PIL import Image
from io import BytesIO
import json


class Supabase:
    client: Client = None

    def connect(self) -> None:
        try:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")

            supabase: Client = create_client(url, key)
            self.client = supabase
        except Exception as e:
            raise CouldNotConnectDB()

    def saveNews(self, news: dict) -> None:
        # Upload Main Image to Supabase Storage
        image = self.uploadImage(news["image"])

        # Upload Content images to Supabase Storage
        for content in news["content"]:
            if content["type"] == "image":
                content["body"] = self.uploadImage(content["body"])

        self.client.table("news").insert(
            {
                "title": news["title"],
                "slug": news["slug"],
                "description": news["description"],
                "created_at": news["publish_date"],
                "image": image,
                "category": news["subject"],
                # python dict to json
                "content": news["content"],
            }
        ).execute()

    def uploadImage(self, image: str) -> str:
        img_name = image.split("/")[-1].split(".")[0]

        r = requests.get(image, stream=True)

        if r.status_code != 200:
            raise Exception("Could not download image")

        # Convert image to webp
        img = Image.open(BytesIO(r.content))
        b = BytesIO()
        img.save(b, format="webp", optimize=True)

        response = self.client.storage.from_("sariyervehaber").upload(
            "images" + "/" + img_name + ".webp", b.getvalue(), {"content-type": "image/webp"}
        )

        if response.status_code == 200:
            public_url = (
                "https://bohpjlknwqcehwlistzx.supabase.co/storage/v1/object/public/sariyervehaber/images/"
                + img_name
                + ".webp"
            )

            return public_url

        return None
