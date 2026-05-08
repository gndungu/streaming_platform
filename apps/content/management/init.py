import requests
from django.conf import settings


class TMDbClient:
    """
    Simple TMDb API client
    """

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.session = requests.Session()
        self.session.params = {
            "api_key": self.api_key,
            "language": "en-US"
        }

    # -------------------------
    # Generic request handler
    # -------------------------
    def _get(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"

        response = self.session.get(url, params=params)

        if response.status_code != 200:
            raise Exception(
                f"TMDb API Error {response.status_code}: {response.text}"
            )

        return response.json()

    # -------------------------
    # Movies
    # -------------------------
    def get_movie(self, movie_id):
        return self._get(f"movie/{movie_id}")

    def search_movies(self, query, page=1):
        return self._get(
            "search/movie",
            params={
                "query": query,
                "page": page
            }
        )

    def get_popular_movies(self, page=1):
        return self._get(
            "movie/popular",
            params={"page": page}
        )

    def get_top_rated_movies(self, page=1):
        return self._get(
            "movie/top_rated",
            params={"page": page}
        )

    # -------------------------
    # TV Series
    # -------------------------
    def get_tv_series(self, tv_id):
        return self._get(f"tv/{tv_id}")

    def search_tv(self, query, page=1):
        return self._get(
            "search/tv",
            params={
                "query": query,
                "page": page
            }
        )

    def get_popular_tv(self, page=1):
        return self._get(
            "tv/popular",
            params={"page": page}
        )

    # -------------------------
    # People
    # -------------------------
    def get_person(self, person_id):
        return self._get(f"person/{person_id}")

    def search_people(self, query, page=1):
        return self._get(
            "search/person",
            params={
                "query": query,
                "page": page
            }
        )

    # -------------------------
    # Genres
    # -------------------------
    def get_movie_genres(self):
        return self._get("genre/movie/list")

    def get_tv_genres(self):
        return self._get("genre/tv/list")

    # -------------------------
    # Trending
    # -------------------------
    def get_trending(self, media_type="all", time_window="day"):
        return self._get(f"trending/{media_type}/{time_window}")