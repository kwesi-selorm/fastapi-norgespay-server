from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import User, UserEntry
from passlib.hash import pbkdf2_sha256 as hash_algo

router = APIRouter(prefix="/api/users", tags=["Users"])

# CREATE NEW USER
@router.post("/")
async def create_user(payload: UserEntry):
    """
    CREATE USER
    """
    json_payload = jsonable_encoder(payload)
    if json_payload["password"] != json_payload["confirm_password"]:
        raise HTTPException(
            status_code=400,
            detail="The provided passwords don't match",
        )
    existing = await User.find_one(
        User.username == json_payload["username"] or User.email == json_payload["email"]
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with this username or email already exists",
        )
    pwd_hash = hash_algo.hash(json_payload["password"])
    document = User(
        **json_payload,
        password_hash=pwd_hash,
    )

    try:
        await document.create()
        return JSONResponse(
            status_code=200, content=f"User {document.username} created successfully"
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to create user")
