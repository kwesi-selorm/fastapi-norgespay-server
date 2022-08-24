from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.models import User
from jwt import ExpiredSignatureError

from utils.jwt_helpers import decode_with_jwt

# tokenUrl is the parameter containing the URL that the client (frontend running in the user's browser) will use to send the username and password to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# GET CURRENTLY LOGGED IN USER
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_with_jwt(token)
        username = payload.get("sub")
        if username is None:
            return credentials_exception
    except JWTError:
        raise credentials_exception
    current_user = await User.find_one(User.username == username)
    if current_user is None:
        raise credentials_exception
    return current_user


# CHECK IF THE USER IS ACTIVE, I.E. THE TOKEN HAS NOT EXPIRED
async def user_is_active(token: str = Depends(oauth2_scheme)):
    try:
        await decode_with_jwt(token)
    except ExpiredSignatureError:
        return False
