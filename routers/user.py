from fastapi import APIRouter, Depends, status, HTTPException
import database
from sqlmodel import Session, select
import model
import schema
from sqlalchemy.exc import IntegrityError
import hashing
from typing import List
import oauth2
router = APIRouter(
    tags= ["Users"]
)


@router.get('/user/me', status_code=status.HTTP_200_OK)
def get_current_user(db: Session = Depends(database.get_session), current_user: model.User = Depends(oauth2.get_current_user)):
    return {
        'user_id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'anime_list': current_user.anime_list
    }

@router.get('/user', status_code=status.HTTP_200_OK, response_model= List[schema.userSchemaShow])
def get_all_users(db: Session = Depends(database.get_session)):
    user= db.exec(select(model.User)).all()
    return user

@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(req: schema.userSchema, db: Session = Depends(database.get_session)):
    new_user= model.User(
        username= req.username,
        email= req.email,
        password= hashing.hash.hash_pass(req.password)
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Username or email already exist")
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Something went wrong, please try again!")

    

@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model= schema.userSchemaShow)
def getUserById(id: int, db: Session = Depends(database.get_session)):
    user= db.exec(select(model.User).where(model.User.id==id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
    
    
        