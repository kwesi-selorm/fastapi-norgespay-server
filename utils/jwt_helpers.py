import os
from datetime import datetime, timedelta
from pprint import pprint

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

load_dotenv()

secret_key = os.getenv("SECRET_KEY")


async def encode_with_jwt(
    payload: dict, selected_expiry: timedelta | None = None
) -> str:
    encoded_token = ""
    # The payload is a dict of the retrieved user from the database (_id, username, password_hash)
    payload_copy = payload.copy()
    if selected_expiry:
        expiry = datetime.utcnow() + selected_expiry
    else:
        expiry = datetime.utcnow() + timedelta(hours=1)
    payload_copy.update({"exp": expiry})
    if secret_key:
        encoded_token = jwt.encode(payload_copy, secret_key, algorithm="HS256")
    return encoded_token


async def decode_with_jwt(token: str):
    # The decoded payload comprises the user's username and the expiry property
    payload: dict = {}
    if secret_key:
        try:
            payload = jwt.decode(token, secret_key, algorithm="HS256")
        except (ExpiredSignatureError, InvalidTokenError) as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Unauthorized to perform the requested operation: {e}",
            )
    return payload
