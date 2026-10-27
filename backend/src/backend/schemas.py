from pydantic import BaseModel


class Movie(BaseModel):
    movid_id: int
    title: str
    genres: str
    tmdb_id: int | None = None
    pic_url: str | None = None


class MovieAndReviews(BaseModel):
    movie_id: int
    title: str
    genres: str
    tmdb_id: int | None = None
    pic_url: str | None = None
    review_score: int | None = None
