from fastapi import APIRouter
import database

router = APIRouter()


@router.get("/healthcheck")
def health_check():
    with database.Session(database.engine) as session:
        session.exec("SELECT 1")
    return {"status": "ok"}