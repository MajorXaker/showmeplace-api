import json

from fastapi import Response, status as http_status, APIRouter, Depends
from sqlalchemy.orm import Session

from utils.db import get_session

healthcheck_router = APIRouter()


@healthcheck_router.get("/healthcheck")
async def healthcheck(response: Response, db: Session = Depends(get_session)):
    try:
        if await db.execute("""SELECT 1"""):
            response.status_code = http_status.HTTP_200_OK
            status = "ok"
        else:
            response.status_code = http_status.HTTP_500_INTERNAL_SERVER_ERROR
            status = "error"
    except BaseException:
        response.status_code = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        status = "error"

    data = json.dumps({"status": status})
    return Response(content=data, media_type="application/json")
