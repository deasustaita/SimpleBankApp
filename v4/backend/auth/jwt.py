from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import dotenv_values
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

config = dotenv_values(".env")

SECRET_KEY = config["JWT_SECRET_KEY"]
ALGORITHM = config["JWT_ALGORITHM"]
TOKEN_EXPIRATION = int(config["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"])
security = HTTPBearer(auto_error=False)

def create_access_token(customer_id: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION)

    payload = {
        "sub": customer_id,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        customer_id = payload.get("sub")

        if not customer_id:
            return None

        return customer_id
    except JWTError:
        return None


def get_current_customer_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    customer_id = decode_access_token(credentials.credentials)

    if not customer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return customer_id