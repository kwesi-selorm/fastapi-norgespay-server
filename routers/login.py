from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from passlib.hash import pbkdf2_sha256 as hash_algo
from utils.jwt_helpers import encode_with_jwt

router = APIRouter(tags=["Login"])


@router.post("/api/login", status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    LOG IN
    """
    existing_user = await User.find_one(User.username == form_data.username)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    json_existing_user: dict = jsonable_encoder(existing_user)
    existing_user_pwd_hash = json_existing_user["password_hash"]
    match = hash_algo.verify(form_data.password, existing_user_pwd_hash)
    if not match:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )

    generated_token = await encode_with_jwt(
        payload={"sub": json_existing_user["username"]}
    )
    return JSONResponse(
        content={
            "access_token": generated_token,
            "token_type": "Bearer",
        },
    )
