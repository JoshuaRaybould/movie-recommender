from fastapi import APIRouter, HTTPException, status

from backend.ai_model import get_rec
from backend.db import ConnectionDep
from backend.main import get_model
from backend.repository import get_movie_by_id
from backend.routes.auth import GetActiveUserDep
from backend.schemas import Movie
from backend.tmdb_api import retrieve_pic

router = APIRouter()

"""
@router.post("/train/{userToken}")
def trainModel():
    df = createDataset()
    global currentModel
    currentModel = createModel(df)
    return True
"""


@router.get("/recommendation/{userToken}")
def getRecommendation(user: GetActiveUserDep, con: ConnectionDep) -> Movie | None:
    rec = get_rec(get_model(), user.user_id)
    rec_id = rec[1]

    movie = get_movie_by_id(con, rec_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if movie.tmdb_id is not None:
        movie.pic_url = retrieve_pic(movie.tmdb_id)

    return movie
