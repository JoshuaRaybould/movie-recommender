from pydantic import BaseModel


class Movie(BaseModel):
    movie_id: int
    title: str
    genres: str
    tmdb_id: int | None = None
    pic_url: str | None = None


class MovieAndReviews(Movie):
    review_score: int | None = None


class User(BaseModel):
    user_id: int
    email: str | None = None
    username: str
    is_disabled: bool = False


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class Rating(BaseModel):
    rating_id: int
    movie_id: int
    rating: int
    # created_at todo
