import requests

from backend.config import get_settings

TMDB_API_KEY = get_settings().tmdb_api_key


# Get picture from TMDB
def retrieve_pic(tmdb_id: int):
    url = "https://api.themoviedb.org/3/movie/" + str(tmdb_id)
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
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
