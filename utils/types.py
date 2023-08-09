from typing import TypedDict, List
from enum import Enum


class NewsPaperHeadLine(TypedDict):
    newspaper_nane: str
    image: str
    created_at: str


class NewsContent(TypedDict):
    type: str
    body: str


class News(TypedDict):
    title: str
    slug: str
    description: str
    publish_date: str
    image: str
    subject: str
    content: List[NewsContent]


class LogType(Enum):
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
