from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import database
import schema
import model
import hashing
import tokenJWT

router= APIRouter(
    tags=["Login"]
)

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def login(req:schema.loginSchema ,db: Session = Depends(database.get_session)):
    user= db.exec(select(model.User).where(model.User.username==req.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Incorrect Username")
    
    if not hashing.hash.verify(req.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    
    access_token_expires = timedelta(minutes=tokenJWT.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokenJWT.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
     )

    return schema.Token(access_token=access_token, token_type="bearer")