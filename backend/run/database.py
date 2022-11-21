from option import *
from sqlalchemy.orm import Session, joinedload
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from datetime import datetime


class code_jobs:
    __tablename__ = "code_jobs"

    id: Optional[int]
    language: str
    code: str

    status: str
    status_update: Optional[datetime]

    output: Optional[str]
    last_read_line: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.language = kwargs.get("language", None)
        self.code = kwargs.get("code", None)
        self.status = kwargs.get("status", None)
        self.status_update = kwargs.get("status_update", None)
        self.output = kwargs.get("output", None)
        self.last_read_line = kwargs.get("last_read_line", None)


def create_run_requst(form: code_jobs, session: Session) -> Result[int, str]:
    try:
        session.add(form)
        session.commit()
        session.refresh(form)
        return Ok(form.id)
    except Exception as e:
        return Err(str(e))
