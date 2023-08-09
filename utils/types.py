from typing import TypedDict, List
from enum import Enum


class NewsPaperHeadLine(TypedDict):
    newspaper_nane: str
    image: str
    created_at: str


class PostContent(TypedDict):
    type: str
    body: str


class Post(TypedDict):
    title: str
    slug: str
    description: str
    created_at: str
    image: str
    category: str
    content: List[PostContent]


class LogType(Enum):
    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"
