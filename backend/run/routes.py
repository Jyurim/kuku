from . import database, schema
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from option import *
import utils
from utils.exception import throwMsg
from utils.session import *

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", dependencies=[Depends(cookie)])
async def main(
    form: schema.run_request,
    db: Session = Depends(utils.database.get_db),
    session_data: SessionData = Depends(verifier),
):
    if session_data.type != 0:
        return throwMsg("권한이 없습니다.")

    form = database.code_jobs(**form.dict(), status="que")
    return database.create_run_requst(form, db).map_err(throwMsg).unwrap()
