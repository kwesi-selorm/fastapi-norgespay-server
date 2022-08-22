from fastapi import APIRouter, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import Contributor, DBContributor

router = APIRouter(prefix="/api/contributors", tags=["Contributors"])

# FIND ONE CONTRIBUTOR
@router.post("/", status_code=200)
async def find_contributor(payload: Contributor):

    """Verify contributor exists"""
    json_payload = jsonable_encoder(payload)
    existing_contributor = await DBContributor.find_one(
        DBContributor.username == json_payload["username"]
    )
    if not existing_contributor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please contribute a salary entry in order to proceed. You will be redirected now...",
        )


# CREATE CONTRIBUTOR
@router.post("/add")
async def create_contributor(payload: Contributor):

    """Create a new contributor"""
    json_payload = jsonable_encoder(payload)
    document = DBContributor(**json_payload)
    try:
        existing = await DBContributor.find_one(
            DBContributor.username == json_payload["username"]
        )
        if existing:
            return
        await DBContributor.create(document)
        return JSONResponse(status_code=201, content=None)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong, please try again later",
        )
