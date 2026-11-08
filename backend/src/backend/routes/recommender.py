from fastapi import APIRouter, HTTPException, status

import backend.main as m
from backend.ai.model import get_model_full, get_rec
from backend.db import ConnectionDep
from backend.repository import get_movie_by_id
from backend.routes.auth import GetActiveUserDep
from backend.schemas import RecommendedMovie
from backend.tmdb_api import retrieve_pic

router = APIRouter()


@router.post("/train", status_code=204)
def trainModel(con: ConnectionDep):
    m.app.state.model = get_model_full(con)


@router.get("/recommendation")
def getRecommendation(
    user: GetActiveUserDep, con: ConnectionDep
) -> list[RecommendedMovie]:
    rec = get_rec(m.get_model(), con, user)
    if rec is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)  # todo

    movie = get_movie_by_id(con, rec["movie_id"])
    if movie is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if movie.tmdb_id is not None:
        movie.pic_url = retrieve_pic(movie.tmdb_id)
    rec_movie = RecommendedMovie.model_validate(
        {"expected_score": rec["expected_score"], **(movie.model_dump())}
    )

    return [rec_movie]
