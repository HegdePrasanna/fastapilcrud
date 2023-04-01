from pydantic import BaseModel
from typing import Optional


class BlogRequest(BaseModel):
    title: str
    body: str
    published: Optional[bool]
