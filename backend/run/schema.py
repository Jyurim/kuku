from pydantic import *
from typing import Optional


class run_request(BaseModel):
    language: str
    code: str
