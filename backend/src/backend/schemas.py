from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        )
    )


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


class Movie(CamelModel):
    movie_id: int
    title: str
    genres: str
    tmdb_id: int | None = None
    pic_url: str | None = None


class Review(CamelModel):
    review_id: int
    user_id: int
    movie_id: int
    rating: int


class MovieAndReview(Movie):
    review: Review | None = None


class RecommendedMovie(Movie):
    expected_score: float


# created_at todo
