from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from typing import Dict
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from typing import Optional

# Replace with a secure secret key
SECRET_KEY = "yXy3mJ82HqLP_NFt8QfB2qLjYhc7u-BiXJz5Sm1KXzGw"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_access_token(token: str) -> Dict:
    """
    Verifies the JWT token and returns the decoded payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        return token
