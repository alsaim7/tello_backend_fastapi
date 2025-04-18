from fastapi import APIRouter, Depends, status
import controllers.animeList
import database
from sqlmodel import Session
import schema
import controllers
from typing import List
import model
import oauth2

router= APIRouter(
    prefix='tello',
    tags=["Anime"]
)

@router.get('/', status_code=status.HTTP_200_OK, response_model= List[schema.animeSchemaShow])
def get_a_list_of_anime(db: Session = Depends(database.get_session)):
    return controllers.animeList.get_all_anime(db)


@router.post('/', status_code= status.HTTP_201_CREATED)
def create_anime(req:schema.animeSchema,db: Session = Depends(database.get_session), current_user: model.User = Depends(oauth2.get_current_user)):
    return controllers.animeList.create_new_anime(req,db, current_user)


@router.get('/{id}', response_model= schema.animeSchemaShow)
def get_anime_by_id(id:int, db: Session = Depends(database.get_session)):
    return controllers.animeList.get_anime_by_id(id,db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_anime(id:int, db: Session = Depends(database.get_session), current_user: model.User = Depends(oauth2.get_current_user)):
    return controllers.animeList.delete_an_anime(id, db, current_user)


@router.patch('/{id}', status_code=status.HTTP_200_OK)
def update_anime(id:int, req:schema.animeSchema, db: Session = Depends(database.get_session), current_user: model.User = Depends(oauth2.get_current_user)):
    return controllers.animeList.update_an_anime(id, req, db, current_user)
    