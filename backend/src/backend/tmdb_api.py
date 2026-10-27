import os

import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")  # todo


# Get picture from TMDB
def retrieve_pic(tmdbId: int):
    url = "https://api.themoviedb.org/3/movie/" + str(tmdbId)
    headers = {
        "Authorization": TMDB_API_KEY,
        "accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            pic = data["poster_path"]
            return pic
        else:
            print("Error:", response.status_code)
            return None
    except:  # todo
        return None
