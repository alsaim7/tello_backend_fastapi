from fastapi import APIRouter

router= APIRouter(
    tags= ["Health_Check"]
)


@router.get('/healthcheck')
def healthcheck():
    return{'status': 'ok'}