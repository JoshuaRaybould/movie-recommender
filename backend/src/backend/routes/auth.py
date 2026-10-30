from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.db import ConnectionDep
from backend.repository import get_user_by_username
from backend.schemas import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
@router.post("/signup/{user_token}")
def signup(user_token: str, con: ConnectionDep) -> User:
    try:
        user = create_user(con, user_token)
    except UserAlreadyExistsErorr:
        raise HTTPException(status_code=409, detail="User (token) already exists")
    return user


@router.get("/signin/{user_token}")
def signin(user_token: str, con: ConnectionDep) -> User:
    user = get_user(con, user_token)
    if not user:
        raise HTTPException(status_code=404, detail="User (token) doesn't exist")
    return user
"""


def decode_token(token):  # -> User
    return "tok"


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


def hash_password(password) -> str | None:
    if password is None:
        return None
    return password  # todo


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], con: ConnectionDep
):
    incorrect_login_message = "Incorrect username or password"
    user = get_user_by_username(con, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=incorrect_login_message,
        )

    hashed_password = hash_password(form_data.password)

    if hashed_password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=incorrect_login_message,
        )

    return {"access_token": user.username, "token_type": "bearer"}


# todo, presumabely the access token should be a proper thing
