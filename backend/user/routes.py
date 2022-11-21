from . import database
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from .schemas import changeuser, createuser, loginuser, originuser
from utils.exception import throwMsg
from fastapi import Response, Depends
from uuid import UUID, uuid4
from utils.session import *
from fastapi.responses import HTMLResponse
from . import templateHtml
from result import Result, Ok, Err, as_result

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def user(email: str, session: Session = Depends(utils.database.get_db)):
    return database.get_user_by_email(email, session)


# user 계성 생성 라우터 함수
@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: createuser, session: Session = Depends(utils.database.get_db)
):
    return database.create_user(user, session).map_err(throwMsg).unwrap()


# 모든 user 정보 보여주는 함수
@router.get("/all")
async def all_user(session: Session = Depends(utils.database.get_db)):
    return session.query(database.User).all()


@router.post("/login")
async def create_session(
    user: loginuser,
    response: Response,
    session: Session = Depends(utils.database.get_db),
):
    user_data = database.login(user, session).map_err(throwMsg).unwrap()
    uuidSession = uuid4()
    data = SessionData(**user_data.dict())

    await sessionStorage.create(uuidSession, data)
    cookie.attach_to_response(response, uuidSession)

    return database.get_user_by_uid(user_data.uid, session).map_err(throwMsg).unwrap()


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(
    session_data: SessionData = Depends(verifier),
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.get_user_by_uid(session_data.uid, session).map_err(throwMsg).unwrap()
    )


@router.put("/update", dependencies=[Depends(cookie)])
async def update_user(
    changeUser: changeuser,
    originUser: originuser,
    session_data: SessionData = Depends(verifier),
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.update_user(changeUser, originUser, session_data.uid, session)
        .map_err(throwMsg)
        .unwrap()
    )


@router.delete("/delete", dependencies=[Depends(cookie)])
async def delete_user(
    user: loginuser, session: Session = Depends(utils.database.get_db)
):
    return database.delete_user(user, session).map_err(throwMsg).unwrap()


@router.post("/logout")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    if session_id in sessionStorage.data:
        await sessionStorage.delete(session_id)

    cookie.delete_from_response(response)
    return "deleted session"


# send email request
@router.post("/sendEmailBySesson", dependencies=[Depends(cookie)])
async def send_email(
    session_data: SessionData = Depends(verifier),
    session: Session = Depends(utils.database.get_db),
):
    return (
        database.emailCertification(session, session_data.uid)
        .map_err(throwMsg)
        .unwrap()
    )


# send email request
@router.post("/sendEmailByEmail/{email}")
async def send_email(email: str, session: Session = Depends(utils.database.get_db)):
    return database.emailCertificationByEmail(session, email).map_err(throwMsg).unwrap()


@router.get("/emailConfirm")
async def email_confirm(token: str, session: Session = Depends(utils.database.get_db)):
    result = database.emailConform(token, session)
    if isinstance(result, Ok):
        return HTMLResponse(
            content=templateHtml.successTemplate(result.unwrap()), status_code=200
        )
    else:
        return HTMLResponse(content=templateHtml.failTemplate(), status_code=200)


# username 중복 검사
@router.get("/check")
async def user(username: str, session: Session = Depends(utils.database.get_db)):
    if database.check_username(username, session):
        return True
    else:
        return False
