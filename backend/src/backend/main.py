from fastapi import FastAPI

from backend.routes import movies

app = FastAPI()
app.include_router(movies.router)
# app.include_router(recommender.router)
