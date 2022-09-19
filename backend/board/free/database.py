from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel ,Relationship
from typing import Optional ,List
from utils.exception import *

class board_free(SQLModel, table=True):
    article_id: Optional[int] = Field(default=None, primary_key=True)
    title : str
    content : str

    userid : int = Field(default=None,foreign_key='user.uid')
    userRel :  "User" = Relationship(back_populates="free")

    created : datetime = Field(default=datetime.now())
    state: int = Field(default=1)  # deleted = 0, normal = 1
    like: int = Field(default=0)
    views: int =Field(default=0)

#create board_free aritcle
def create_article(object_in: board_free, db: Session) -> Result:
    try:
        article = board_free.from_orm(object_in)
        db.add(article)
        db.commit()
        db.refresh(article)
        return Ok(article)

    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail = "malformed form data"))
        elif "foreign key constraint fails" in err_msg:
            return Err(DefaultException(detail = "user id is not a valid"))
        return Err(DefaultException(detail = "unknown error"))


# get all user objects
def get_all_article_free(db: Session):
    return db.query(board_free).all()