from datetime import UTC, datetime, timedelta
from sqlite3 import Connection
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from backend.config import SettingDep
from backend.db import ConnectionDep
from backend.exceptions import UserAlreadyExistsErorr
from backend.repository import create_user, get_user_by_username
from backend.schemas import Token, User, UserCreate, UserInDB

router = APIRouter()

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return password_hash.hash(password)


def authenticate_user(con: Connection, username: str, password: str) -> UserInDB | None:
    user = get_user_by_username(con, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(settings: SettingDep, data: dict) -> str:
    expires_delta = timedelta(minutes=settings.access_token_expire)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    con: ConnectionDep,
    settings: SettingDep,
) -> Token:
    user = authenticate_user(con, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(settings, data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup")
def signup(user_details: UserCreate, con: ConnectionDep, settings: SettingDep) -> Token:
    hashed_password = get_password_hash(user_details.password)
    try:
        user = create_user(con, user_details.username, hashed_password)
    except UserAlreadyExistsErorr:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username taken"
        )

    access_token = create_access_token(settings, data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: SettingDep,
    con: ConnectionDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(con, username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@router.get("/users/me")
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user
