from datetime import datetime, timedelta
from typing import Union, Any, Optional
from jose import jwt, JWTError
from app.core.config import setting


def create_access_token(subject: Union[str, Any], role: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now() + (expires_delta or timedelta(minutes=setting["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role
    }
    return jwt.encode(to_encode, setting["secret_key"], algorithm=setting["algorithm"])

def decode_access_token(token: str):
    try:
        return jwt.decode(token, setting["secret_key"], algorithms=[setting["algorithm"]])
    except JWTError:
        raise ValueError("Invalid token")