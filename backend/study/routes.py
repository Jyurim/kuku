### 전체적인 구조: 여러개의 코스 (알고리즘, 그래픽스, 컴퓨터구조) -> 여러개의 챕터 (Brute Force, Sorting)


from . import database, schema
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from utils.session import *
from board.free.like.database import *
from board.free.comment.database import *

router = APIRouter(
    prefix="/study",
    tags=["study"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_all_course(session: Session = Depends(utils.database.get_db)):
    return database.list_course(session).map_err(throwMsg).unwrap()


@router.get("/head-chapters/")
async def list_head_chapter(session: Session = Depends(utils.database.get_db)):
    def flatten_course(article: List[database.lecture_chapter]):
        return tuple(
            map(
                lambda x: {
                    "no": x.no,
                    "title": x.title,
                    "category": x.category,
                    "parent_id": x.parent_id,
                    "course_id": x.course_id,
                    "course_title": x.lectureRel.title,
                    "course_slug": x.lectureRel.slug,
                },
                article,
            )
        )

    def join_supported_languages(article: tuple):
        return tuple(
            map(
                lambda x: {
                    **x,
                    "supported_languages": database.list_chapter_languages(
                        x["course_slug"], x["no"], session
                    ).unwrap_or([]),
                },
                article,
            )
        )

    return (
        database.list_head_chapter(session)
        .map(flatten_course)
        .map(join_supported_languages)
        .map_err(throwMsg)
        .unwrap()
    )


@router.get("/courses")
async def list_course(session: Session = Depends(utils.database.get_db)):
    return database.list_course(session).map_err(throwMsg).unwrap()


@router.get("/categories")
async def list_category(session: Session = Depends(utils.database.get_db)):
    return database.list_category(session).map_err(throwMsg).unwrap()


@router.get("/{course_slug}/list")
async def list_course_chapter(
    course_slug: str, session: Session = Depends(utils.database.get_db)
):
    class course_tree:
        no: Optional[int]
        title: str
        category: str
        parent_id: Optional[int]
        children: List["course_tree"]

        def __init__(self, data: database.lecture_chapter):
            self.no = data.no
            self.title = data.title
            self.category = data.category
            self.parent_id = data.parent_id
            self.children = []

    chapters = database.list_chapter(course_slug, session).map_err(throwMsg).unwrap()
    chapater_dict = {}

    for chapter in chapters:
        chapater_dict[chapter.no] = course_tree(chapter)

    chapter_list = []
    for (idx, chapter) in chapater_dict.items():
        if chapter.parent_id == None:
            chapter_list.append(chapter)
        else:
            chapater_dict[chapter.parent_id].children.append(chapter)

    return chapter_list


# write new article
# @router.post("/{course_slug}/write")
# async def write_course_chapter(
#     course_slug: str,
#     article: database.lecture_chapter,
#     session: Session = Depends(utils.database.get_db),
# ):
#     return (
#         database.write_chapter(course_slug, article, session).map_err(throwMsg).unwrap()
#     )


@router.get("/chapter/{chapter}")
async def get_chapter_info(
    chapter: int, session: Session = Depends(utils.database.get_db)
):
    class chapter_info:
        no: int
        title: str
        category: str
        parent_id: Optional[int]
        course_id: int
        course_title: str
        course_slug: str

        def __init__(self, data: database.lecture_chapter):
            self.no = data.no
            self.title = data.title
            self.category = data.category
            self.parent_id = data.parent_id
            self.course_id = data.course_id
            self.course_title = data.lectureRel.title
            self.course_slug = data.lectureRel.slug

    return (
        database.get_chapter_info(chapter, session)
        .map(lambda item: chapter_info(item))
        .map_err(throwMsg)
        .unwrap()
    )


@router.get("/{course_slug}/{chapter}/")
async def list_article(
    course_slug: str, chapter: int, session: Session = Depends(utils.database.get_db)
):
    return (
        database.list_article(course_slug, chapter, session).map_err(throwMsg).unwrap()
    )


@router.post("/{course_slug}/", dependencies=[Depends(cookie)])
async def write_article(
    course_slug: str,
    article_form: schema.form_article,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    if session_data.is_admin == "N":
        return throwMsg("권한이 없습니다.")

    course = database.get_course_info(course_slug, session).map_err(throwMsg).unwrap()
    course_id = course.course_id

    chapter = None

    if article_form.chapter_id != None:
        chapter = (
            database.get_chapter_info(article_form.chapter_id, session)
            .map_err(throwMsg)
            .unwrap()
        )

        chapter.__setattr__("title", article_form.title)
    else:
        chapter = (
            database.get_chapter_by_title(course_id, article_form.title, session)
            .map_err(throwMsg)
            .unwrap()
            .unwrap_or(
                database.lecture_chapter(course_id=course_id, **article_form.dict())
            )
        )

    if article_form.parent_id != None:
        if article_form.chapter_id != None and article_form.parent_id == chapter.no:
            return throwMsg("자기 자신을 부모로 지정할 수 없습니다.")

        chapter.__setattr__(
            "parent_id",
            article_form.parent_id,
        )

    chapter = database.create_chapter(chapter, session).unwrap_or(None)

    if chapter is None:
        return throwMsg("챕터 생성 또는 조회 실패")

    def update_article(article: database.lecture_article):
        for (k, v) in article_form.dict().items():
            if k not in article.dict().keys():
                continue

            article.__setattr__(k, v)

        return article

    article: database.lecture_article = (
        database.get_article(chapter.no, article_form.language, session)
        .map_err(throwMsg)
        .unwrap()
        .map(update_article)
        .unwrap_or(
            database.lecture_article(
                chapter_id=chapter.no,
                language=article_form.language,
                code=article_form.code,
                content=article_form.content,
            )
        )
    )

    return database.create_article(article, session).map_err(throwMsg).unwrap()


@router.put("/{course_slug}/{chapter}/", dependencies=[Depends(cookie)])
async def update_article(
    course_slug: str,
    chapter: int,
    article: schema.form_article,
    session: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    if session_data.is_admin != "N":
        return throwMsg("권한이 없습니다.")

    return (
        database.update_article(course_slug, chapter, article, session)
        .map_err(throwMsg)
        .unwrap()
    )
