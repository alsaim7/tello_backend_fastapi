from fastapi import APIRouter

router = APIRouter()


@router.api_route("/healthcheck", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}