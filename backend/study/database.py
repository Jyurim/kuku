from option import *
from sqlalchemy.orm import Session, joinedload
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *


# lecture -> course_id, title, slug, description
class lecture(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str
    description: str
    chapterRel: "lecture_chapter" = Relationship(back_populates="lectureRel")


# lecture_chapter -> no, title, content, category, parent_id (null), course_id
class lecture_chapter(SQLModel, table=True):
    no: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str
    parent_id: Optional[int] = Field(default=None)
    course_id: int = Field(default=None, foreign_key="lecture.course_id")
    lectureRel: "lecture" = Relationship(back_populates="chapterRel")
    articleRel: "lecture_article" = Relationship(back_populates="chapterRel")


# lecture_article -> no, lecture_article_id, language, code
class lecture_article(SQLModel, table=True):
    no: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: int = Field(default=None, foreign_key="lecture_chapter.no")
    chapterRel: lecture_chapter = Relationship(back_populates="articleRel")
    language: str
    code: str
    content: str


### CRUD 순서대로 작성함
def create_chapter(chapter: lecture_chapter, db: Session):
    try:
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
        return Ok(chapter)
    except Exception as e:
        print(e)
        return Err(str(e))


def create_article(article: lecture_article, db: Session):
    try:
        db.add(article)
        db.commit()
        db.refresh(article)
        return Ok(article)
    except Exception as e:
        print(e)
        return Err(str(e))


### 단일 Row를 가져오는건 get, 여러 Row를 가져오는건 list
def list_course(db: Session):
    try:
        return Ok(db.query(lecture).all())
    except Exception as e:
        return Err(str(e))


def list_head_chapter(db: Session):
    try:
        return Ok(
            db.query(lecture_chapter)
            .filter(lecture_chapter.parent_id == None)
            .options(joinedload(lecture_chapter.lectureRel))
            .all()
        )
    except Exception as e:
        print(e)
        return Err(str(e))


def list_chapter(course: str, db: Session):
    try:
        # get course id from lecture
        course_data = db.query(lecture).filter(lecture.slug == course).first()
        if course_data is None:
            return Err("Course not found")

        course_id = course_data.course_id

        # get chapter list from lecture_article
        return Ok(
            db.query(lecture_chapter)
            .filter(lecture_chapter.course_id == course_id)
            .all()
        )

    except Exception as e:
        return Err(str(e))


def list_category(db: Session):
    try:
        return Ok(
            db.query(lecture_chapter.category).distinct(lecture_chapter.category).all()
        )
    except Exception as e:
        return Err(str(e))


def list_chapter_languages(course_slug: int, chapter: int, db: Session) -> tuple[str]:
    try:
        return Ok(
            tuple(
                map(
                    lambda x: x.language,
                    db.query(lecture_article.language)
                    .filter(lecture_article.chapter_id == chapter)
                    .join(lecture_article.chapterRel)
                    .join(lecture_chapter.lectureRel)
                    .filter(lecture.slug == course_slug)
                    .distinct()
                    .all(),
                )
            )
        )
    except Exception as e:
        return Err(str(e))


def get_course_info(course_slug: str, db: Session):
    try:
        return Ok(db.query(lecture).filter(lecture.slug == course_slug).first())
    except Exception as e:
        return Err("존재하지 않는 강의입니다.")


def get_chapter_info(chapter: int, db: Session):
    try:
        return Ok(
            db.query(lecture_chapter)
            .filter(lecture_chapter.no == chapter)
            .options(joinedload(lecture_chapter.lectureRel))
            .first()
        )
    except Exception as e:
        return Err(str(e))


def get_chapter_by_title(
    course_id: int, title: str, db: Session
) -> Result[Option[lecture_chapter], str]:
    try:
        data = (
            db.query(lecture_chapter)
            .filter(lecture_chapter.course_id == course_id)
            .filter(lecture_chapter.title == title)
            .all()
        )

        if len(data) == 0:
            return Ok(Option.NONE())

        return Ok(Option.Some(data[0]))

    except Exception as e:
        return Err(str(e))


def list_article(course_slug: int, chapter: int, db: Session):
    try:
        return Ok(
            db.query(lecture_article)
            .filter(lecture_article.chapter_id == chapter)
            .join(lecture_article.chapterRel)
            .join(lecture_chapter.lectureRel)
            .filter(lecture.slug == course_slug)
            .all()
        )
    except Exception as e:
        return Err(str(e))


def get_article(
    chapter: int, language: str, db: Session
) -> Result[Option[lecture_article], str]:
    try:
        data = (
            db.query(lecture_article)
            .filter(lecture_article.chapter_id == chapter)
            .filter(lecture_article.language == language)
            .limit(1)
            .all()
        )
        if len(data) == 0:
            return Ok(Option.NONE())

        return Ok(Option.Some(data[0]))

    except Exception as e:
        return Err(str(e))
