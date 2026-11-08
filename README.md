# Movie Recommender

A full-stack web app that recommends films from your own ratings. Users sign up, search a catalogue of films, rate the ones they've seen out of 10, and get personalised recommendations from a collaborative-filtering model.

The code here is written entirely by me with some guidance from LLMs to help ensure I was doing things properly and learning effectively. This README is the only thing written directly by CLAUDE.

> **Status:** work in progress.

## How it works

- **Data:** the film catalogue and ratings come from the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. On startup the backend loads the catalogue into a SQLite database. Poster images are fetched from [TMDB](https://www.themoviedb.org/).
- **Model:** recommendations come from an **SVD matrix factorisation** model (via `scikit-surprise`). The model trains on the MovieLens ratings and the ratings the app's users have entered, so it learns each user's tastes as they rate more films.
- **Hyperparameter tuning:** [`ai/train.py`](backend/src/backend/ai/train.py) runs a 5-fold cross-validated grid search over latent factors and training epochs, scoring each by RMSE. The production model uses the best settings it finds (25 factors, 25 epochs).
- **Serving:** for each user the backend predicts a score for every film they haven't rated, keeps the top candidates in a heap, and returns them one at a time with the predicted score.

## Tech stack

| Layer    | Tools |
|----------|-------|
| Backend  | Python, FastAPI, Pydantic, SQLite |
| ML       | scikit-surprise (SVD), pandas, NumPy, scikit-learn |
| Auth     | JWT bearer tokens (PyJWT), Argon2 password hashing (pwdlib) |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, TanStack Query, React Router, Zod |
| Tooling  | uv, Ruff, mypy, ESLint |

## Project structure

```
backend/src/backend/
  main.py          # FastAPI app; loads the DB and trains the model on startup
  routes/          # auth, movie search/rating, and recommendation endpoints
  ai/              # model training and recommendation logic
  repository.py    # SQL queries
  tmdb_api.py      # poster lookup via the TMDB API
frontend/movie-recommender/src/
  pages/           # log in, sign up, search & rate, recommendations
  auth/            # auth context / useAuth hook
```

## Running locally

**Prerequisites:** Python 3.14+, [uv](https://docs.astral.sh/uv/), Node.js, a [TMDB API read access token](https://developer.themoviedb.org/), and a MovieLens dataset (e.g. `ml-latest-small`) containing `movies.csv`, `ratings.csv` and `links.csv`.

1. **Backend.** Create `backend/.env`:

   ```env
   SECRET_KEY=<random string for signing JWTs>
   DATABASE_PATH=movies.db
   MOVIE_DATA_PATH=path/to/ml-latest-small/   # trailing slash required
   TMDB_API_KEY=<TMDB read access token>
   ```

   Then start the API:

   ```bash
   cd backend
   uv sync
   uv run fastapi dev src/backend/main.py
   ```

   The API runs at `http://localhost:8000`. Interactive docs are at `/docs`.

2. **Frontend.** In a second terminal:

   ```bash
   cd frontend/movie-recommender
   npm install
   npm run dev
   ```

   Vite proxies `/api` requests to the backend.

## Acknowledgements

This project uses the MovieLens dataset:

F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems (TiiS)* 5, 4: 19:1–19:19. https://doi.org/10.1145/2827872

Film posters and metadata are provided by [TMDB](https://www.themoviedb.org/). This product uses the TMDB API but is not endorsed or certified by TMDB.
