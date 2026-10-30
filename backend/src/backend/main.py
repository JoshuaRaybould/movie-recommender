from fastapi import FastAPI

from backend.routes import auth, movies

app = FastAPI()
app.include_router(auth.router)
app.include_router(movies.router)
# app.include_router(recommender.router)
