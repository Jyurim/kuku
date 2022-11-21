from pydantic import *
from typing import Optional


class form_article(BaseModel):
    parent_id: Optional[int]
    chapter_id: Optional[int]
    language: str
    category: str
    title: str

    content: str
    code: str
