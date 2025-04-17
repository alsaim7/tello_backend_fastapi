from fastapi import Depends, HTTPException, status
from typing import Annotated
import jwt
import tokenJWT
import schema
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
import database
import model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(database.get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, tokenJWT.SECRET_KEY, algorithms=[tokenJWT.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.exec(select(model.User).where(model.User.username == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user