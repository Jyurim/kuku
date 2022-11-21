from option import *
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from .security import get_password_hash, verify_password
from utils.exception import *
from .schemas import loginuser, UserInformation
from typing import TYPE_CHECKING
from sendgrid.helpers.mail import Mail, Email, To, Content
import sendgrid
from config_default import Config
from . import templateHtml

if TYPE_CHECKING:
    from board.free.database import board_free
    from board.qna.database import board_qna
    from board.qna.like.database import board_qna_like
    from board.free.like.database import board_free_like
    from board.free.comment.database import board_free_comment
from utils.token import verify_token, token_generator_by_email
from result import Result, Ok, Err


class User(SQLModel, table=True):

    uid: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column_kwargs={"name": "username", "unique": True})
    password: str
    email: EmailStr = Field(sa_column_kwargs={"name": "email", "unique": True})
    created: datetime = Field(default=datetime.now())
    type: int = Field(
        default=0
    )  # emailuncormfirmed = 0, emailconformed = 1,  upser = 2
    state: int = Field(default=1)  # deleted = 0, normal = 1

    is_admin: str = Field(default="N")

    # board_free <-> user table
    free: List["board_free"] = Relationship(back_populates="userRel")
    qna: List["board_qna"] = Relationship(back_populates="userRel")
    qna_likeRel: List["board_qna_like"] = Relationship(back_populates="userRel")
    free_likeRel: List["board_free_like"] = Relationship(back_populates="userRel")
    comment: List["board_free_comment"] = Relationship(back_populates="userRel")


# get user by email
def get_user_by_email(email: str, db: Session):
    return db.query(User).filter_by(email=email).first()


# get user by uid
def get_user_by_uid(uid: int, db: Session) -> Result:
    user = db.query(User).filter_by(uid=uid).first()
    if user is not None:
        return Ok(
            UserInformation(
                userid=user.uid,
                username=user.username,
                email=user.email,
                created=user.created,
            )
        )
    else:
        return Err(NotFound())


# create_user
def create_user(object_in: User, db: Session) -> Result:
    try:
        object_in.password = get_password_hash(object_in.password)
        user = User.from_orm(object_in)
        db.add(user)
        if isinstance(emailCertificationByEmail(db, object_in.email), Err):
            return Err(DefaultException(detail="email send error"))
        db.commit()
        db.refresh(user)
        return Ok(
            UserInformation(
                userid=user.uid,
                username=user.username,
                email=user.email,
                created=user.created,
            )
        )

    except Exception as e:
        err_msg = str(e).lower()

        if "username_unique" in err_msg:
            return Err(AlreadyExists())
        if "email_unique" in err_msg:
            return Err(AlreadyExists())
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        if "is not a valid" in err_msg:
            return Err(DefaultException(detail="form data is not a valid"))
        return Err(DefaultException(detail="unknown error"))


# get all user objects
def get_all_user(db: Session):
    return db.query(User).all()


# login
def login(object_in: loginuser, db: Session) -> Result:
    user = db.query(User).filter_by(email=object_in.email, state=1).first()
    if user is None:
        return Err(NotFound())
    if not verify_password(object_in.password, user.password):
        return Err(NotFound())
    return Ok(user)


def emailCertification(db: Session, uid: int) -> Result:
    try:
        email = db.query(User).filter_by(uid=uid, state=1).first()
        if email is None:
            return Err(NotFound())
        sg = sendgrid.SendGridAPIClient(api_key=Config.sendGridKey)
        from_email = Email("noreply@eyo.kr")  # Change to your verified sender
        to_email = To(email.email)  # Change to your recipient
        subject = "KUKU 회원가입 인증 메일입니다."
        if isinstance(token_generator_by_email(email.email), Ok):
            token = str(token_generator_by_email(email.email).unwrap())
        else:
            return Err(DefaultException(detail="token generator error"))
        content = Content("text/html", templateHtml.emailTemplate(token))
        mail = Mail(from_email, to_email, subject, content)
        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if str(response.status_code).lower() in "error":
            return Err(DefaultException(detail="email send error"))
        else:
            return Ok("email send success")
    except Exception as e:
        return Err(DefaultException(detail="unknown error"))


def emailCertificationByEmail(db: Session, email: str) -> Result:
    try:
        sg = sendgrid.SendGridAPIClient(api_key=Config.sendGridKey)
        from_email = Email("noreply@eyo.kr")  # Change to your verified sender
        to_email = To(email)  # Change to your recipient
        subject = "KUKU 회원가입 인증 메일입니다."
        if isinstance(token_generator_by_email(email), Ok):
            token = str(token_generator_by_email(email).unwrap())
        else:
            return Err(DefaultException(detail="token generator error"))
        content = Content("text/html", templateHtml.emailTemplate(token))
        mail = Mail(from_email, to_email, subject, content)
        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if str(response.status_code).lower() in "error":
            return Err(DefaultException(detail="email send error"))
        else:
            return Ok("email send success")
    except Exception as e:
        return Err(DefaultException(detail="unknown error"))


def emailConform(token: str, db: Session) -> Result:
    try:
        if isinstance(verify_token(token), Ok):
            email = verify_token(token).unwrap()
        else:
            return Err(DefaultException(detail="token verify error"))
        user = db.query(User).filter_by(email=email, state=1).first()
        if user is None:
            return Err(NotFound())
        check = (
            db.query(User).filter_by(email=email, state=1).update({"type": 1})
        ) == 1
        if check is False:
            return Err(DefaultException(detail="update err"))
        db.commit()
        return Ok(str(user.username))
    except Exception as e:
        return Err(DefaultException(detail="unknown error"))


def emailCertification(db: Session, uid: int) -> Result:
    try:
        email = db.query(User).filter_by(uid=uid).first()
        if email is None:
            return Err(NotFound())
        sg = sendgrid.SendGridAPIClient(api_key=Config.sendGridKey)
        from_email = Email("noreply@eyo.kr")  # Change to your verified sender
        to_email = To(email.email)  # Change to your recipient
        subject = "Sending with SendGrid is Fun"
        if isinstance(token_generator_by_email(email.email), Ok):
            token = str(token_generator_by_email(email.email).unwrap())
        else:
            return Err(DefaultException(detail="token generator error"))
        content = Content("text/html", templateHtml.emailTemplate(token))
        mail = Mail(from_email, to_email, subject, content)
        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if str(response.status_code).lower() in "error":
            return Err(DefaultException(detail="email send error"))
        else:
            return Ok("email send success")
    except Exception as e:
        return Err(DefaultException(detail="unknown error"))


def emailCertificationByEmail(db: Session, email: str) -> Result:
    try:
        check = db.query(User).filter_by(email=email).first()
        if check is None:
            return Err(NotFound())
        sg = sendgrid.SendGridAPIClient(api_key=Config.sendGridKey)
        from_email = Email("noreply@eyo.kr")  # Change to your verified sender
        to_email = To(email)  # Change to your recipient
        subject = "Sending with SendGrid is Fun"
        if isinstance(token_generator_by_email(email), Ok):
            token = str(token_generator_by_email(email).unwrap())
        else:
            return Err(DefaultException(detail="token generator error"))
        content = Content("text/html", templateHtml.emailTemplate(token))
        mail = Mail(from_email, to_email, subject, content)
        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if str(response.status_code).lower() in "error":
            return Err(DefaultException(detail="email send error"))
        else:
            return Ok("email send success")
    except Exception as e:
        return Err(DefaultException(detail="unknown error"))


def emailConform(token: str, db: Session) -> Result:
    try:
        print(token)
        if isinstance(verify_token(token), Ok):
            email = verify_token(token).unwrap()
        else:
            return Err(DefaultException(detail="token verify error"))
        print(email)
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            return Err(NotFound())
        check = (db.query(User).filter_by(email=email).update({"type": 1})) == 1
        if check is False:
            return Err(DefaultException(detail="update err"))
        db.commit()
        return Ok(str(user.username))
    except Exception as e:
        return Err(DefaultException(detail="unknown error"))


# update_user
def update_user(change: User, origin: User, originuid: str, db: Session) -> Result:
    try:
        user = db.query(User).filter_by(uid=originuid).first()
        if user is None:
            return Err(NotFound())
        if not verify_password(origin.password, user.password):
            return Err(NotAuthorized())

        if change.email != "":
            user.email = change.email
        if change.username != "":
            user.username = change.username
        if change.password != "":
            user.password = get_password_hash(change.password)

        db.add(user)
        db.commit()
        db.refresh(user)
        return Ok(user.uid)

    except Exception as e:
        err_msg = str(e).lower()
        if "data too long" in err_msg:
            return Err(DefaultException(detail="malformed form data"))
        if "is not a valid" in err_msg:
            return Err(DefaultException(detail="form data is not a valid"))
        return Err(DefaultException(detail="unknown error"))


# delete user
def delete_user(object_in: loginuser, db: Session) -> Result:
    user = db.query(User).filter_by(email=object_in.email, state=1).first()
    if user is None:
        return Err(NotFound())
    if not verify_password(object_in.password, user.password):
        return Err(NotFound())
    user.state = 0
    db.commit()
    db.refresh(user)
    return Ok(user.state)


# check username
def check_username(username: str, db: Session) -> Result:
    user = db.query(User).filter_by(username=username, state=1).first()
    if user is not None:
        return Err(AlreadyExists())
    else:
        return Ok(True)
