import model
from sqlmodel import select, func,or_
from fastapi import HTTPException, status

def get_all_anime(db):
    anime= db.exec(select(model.Anime)).all()
    return anime



def create_new_anime(req, db, current_user):
    newAnime= model.Anime(
        anime_name= req.anime_name,
        anime_description= req.anime_description,
        user_id= current_user.id
    )
    db.add(newAnime)
    db.commit()
    db.refresh(newAnime)
    return newAnime



def search_story(search, db):
    results = db.query(model.Anime).join(model.User).filter(
    or_(
        model.Anime.anime_name.ilike(f"%{search}%"),
        model.User.username.ilike(f"%{search}%")
    )
    ).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No search result found for [{search}]')
    return results



def get_anime_by_id(id,db):
    anime= db.exec(select(model.Anime).where(model.Anime.id==id)).first()
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No anime found with id no {id}")
    return anime



def delete_an_anime(id, db, current_user):
    anime= db.exec(select(model.Anime).where(model.Anime.id==id)).first()
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No anime found with id no {id}")
    
    if current_user.id!=anime.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete someone else post")

    db.delete(anime)
    db.commit()
    return {"message": "Anime deleted successfully"}



def update_an_anime(id, req, db, current_user):
    anime= db.exec(select(model.Anime).where(model.Anime.id==id)).first()
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No anime found with id no {id}")
    if req.anime_name:
        anime.anime_name=req.anime_name
    if req.anime_description:
        anime.anime_description=req.anime_description

    if current_user.id!=anime.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't edit someone else post")
    
    db.add(anime)
    db.commit()
    db.refresh(anime)
    return anime