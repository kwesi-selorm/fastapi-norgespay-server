from pprint import pprint

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import User, UserLogin
from passlib.hash import pbkdf2_sha256 as hash_algo

router = APIRouter(tags=["Login"])


@router.post("/api/login")
async def login(payload: UserLogin):
    """
    LOG IN
    """
    json_payload = jsonable_encoder(payload)
    existing_user = await User.find_one(User.username == json_payload["username"])
    json_existing_user: dict = jsonable_encoder(existing_user)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user_pwd_hash = json_existing_user["password_hash"]
    match = hash_algo.verify(json_payload["password"], existing_user_pwd_hash)
    if match:
        # Add functionality to append token to be returned to the user
        return JSONResponse(
            status_code=200,
            content={
                "username": json_existing_user["username"],
                "token": "token",
            },
        )
    raise HTTPException(
        status_code=400,
        detail="Invalid username or password",
    )
