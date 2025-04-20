from fastapi import APIRouter, status
from sqlalchemy import text
import database

router = APIRouter(
    tags=["HealthCheck"]
)

@router.get("/healthcheck", status_code=status.HTTP_200_OK)
def health_check():
    try:
        with database.Session(database.engine) as session:
            session.exec(text("SELECT 1"))  # Use text() to define raw SQL query
        return {"status": "ok"}
    except Exception as e:
        # Return a more detailed error message
        return {"status": "error", "message": str(e)}