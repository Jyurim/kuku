from option import *
from utils.exception import *
from config_default import Config
import jwt
from result import Result, Ok, Err
from urllib import parse


def token_generator_by_email(email: str) -> Result:
    try:
        token_data = {"email": email}
        token = jwt.encode(token_data, Config.session_key, algorithm="HS256")
        token = parse.quote(token)
        return Ok(token)
    except Exception as e:
        return Err(str(e))


def verify_token(token: str) -> Result:
    try:
        token_data = jwt.decode(token, Config.session_key, algorithms=["HS256"])
        return Ok(token_data.get("email"))
    except Exception as e:
        return Err(str(e))
