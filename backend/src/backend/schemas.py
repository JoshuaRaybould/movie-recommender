from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        )
    )


class Movie(CamelModel):
    movie_id: int
    title: str
    genres: str
    tmdb_id: int | None = None
    pic_url: str | None = None


class MovieAndReview(Movie):
    user_id: int
    review_score: int


class User(CamelModel):
    user_id: int
    email: str | None = None
    username: str
    is_disabled: bool = False


class UserInDB(User):
    hashed_password: str


class UserCreate(CamelModel):
    username: str
    password: str
    email: str | None = None


class Token(CamelModel):
    access_token: str
    token_type: str


class Rating(CamelModel):
    rating_id: int
    movie_id: int
    rating: int


# created_at todo


class UserMovieRating(CamelModel):
    user_id: int
    movie_id: int
    rating: int
