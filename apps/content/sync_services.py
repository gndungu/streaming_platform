from django.utils import timezone

from apps.content.tmdb_client import TMDbClient
from apps.streaming.models import HLSStream
from apps.content.models import (
    Movie,
    TVSeries,
    Season,
    Episode,
    Genre,
    Keyword,
    ProductionCompany,
    Country,
    Language,
    VideoSource
)


client = TMDbClient()


# ---------------------------
# Helper: genres sync
# ---------------------------
def sync_genres(genres_data, model):
    objs = []

    for g in genres_data:
        obj, _ = model.objects.get_or_create(
            tmdb_id=g["id"],
            defaults={
                "name": g["name"],
                "slug": g["name"].lower().replace(" ", "-")
            }
        )
        objs.append(obj)

    return objs


# ---------------------------
# MOVIE SYNC
# ---------------------------
def sync_movie(tmdb_id):
    data = client.get_movie(tmdb_id)

    movie, created = Movie.objects.update_or_create(
        tmdb_id=data["id"],
        defaults={
            "imdb_id": data.get("imdb_id"),
            "title": data.get("title"),
            "original_title": data.get("original_title"),
            "tagline": data.get("tagline", ""),
            "overview": data.get("overview", ""),
            "release_date": data.get("release_date"),
            "runtime": data.get("runtime"),
            "budget": data.get("budget"),
            "revenue": data.get("revenue"),
            "vote_average": data.get("vote_average", 0),
            "vote_count": data.get("vote_count", 0),
            "popularity": data.get("popularity", 0),
            "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else "",
            "backdrop_path": f"https://image.tmdb.org/t/p/w1280{data.get('backdrop_path')}" if data.get("backdrop_path") else "",
            "status": data.get("status", "released"),
            "last_tmdb_sync": timezone.now(),
        }
    )

    # Genres
    if "genres" in data:
        movie.genres.set(sync_genres(data["genres"], Genre))

    # Production companies
    if "production_companies" in data:
        companies = []
        for c in data["production_companies"]:
            obj, _ = ProductionCompany.objects.get_or_create(
                tmdb_id=c["id"],
                defaults={
                    "name": c["name"],
                    "logo_path": c.get("logo_path", ""),
                    "origin_country": c.get("origin_country", "")
                }
            )
            companies.append(obj)
        movie.production_companies.set(companies)

    # Countries
    if "production_countries" in data:
        countries = []
        for c in data["production_countries"]:
            obj, _ = Country.objects.get_or_create(
                iso_3166_1=c["iso_3166_1"],
                defaults={"name": c["name"]}
            )
            countries.append(obj)
        movie.production_countries.set(countries)
    
    create_video_sources(
        content_type="movie",
        content_id=movie.id
    )

    return movie


# ---------------------------
# TV SERIES SYNC
# ---------------------------
def sync_tv_series(tmdb_id):
    data = client.get_tv_series(tmdb_id)

    series, created = TVSeries.objects.update_or_create(
        tmdb_id=data["id"],
        defaults={
            "name": data.get("name"),
            "original_name": data.get("original_name"),
            "overview": data.get("overview", ""),
            "first_air_date": data.get("first_air_date"),
            "last_air_date": data.get("last_air_date"),
            "number_of_seasons": data.get("number_of_seasons", 0),
            "number_of_episodes": data.get("number_of_episodes", 0),
            "vote_average": data.get("vote_average", 0),
            "vote_count": data.get("vote_count", 0),
            "popularity": data.get("popularity", 0),
            "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else "",
            "backdrop_path": f"https://image.tmdb.org/t/p/w1280{data.get('backdrop_path')}" if data.get("backdrop_path") else "",
            "status": data.get("status", "returning"),
            "last_tmdb_sync": timezone.now(),
        }
    )

    # Genres
    if "genres" in data:
        series.genres.set(sync_genres(data["genres"], Genre))

    # Seasons + Episodes
    tv_details = client.get_tv_series(tmdb_id)

    for season_data in tv_details.get("seasons", []):
        season, _ = Season.objects.update_or_create(
            tmdb_id=season_data["id"],
            series=series,
            season_number=season_data["season_number"],
            defaults={
                "name": season_data.get("name", ""),
                "overview": season_data.get("overview", ""),
                "air_date": season_data.get("air_date"),
                "episode_count": season_data.get("episode_count", 0),
                "poster_path": f"https://image.tmdb.org/t/p/w500{season_data.get('poster_path')}" if season_data.get("poster_path") else "",
            }
        )

        # Episodes
        season_detail = client._get(f"tv/{tmdb_id}/season/{season.season_number}")

        for ep in season_detail.get("episodes", []):
            Episode.objects.update_or_create(
                tmdb_id=ep["id"],
                season=season,
                episode_number=ep["episode_number"],
                defaults={
                    "name": ep.get("name"),
                    "overview": ep.get("overview", ""),
                    "air_date": ep.get("air_date"),
                    "runtime": ep.get("runtime"),
                    "still_path": f"https://image.tmdb.org/t/p/w500{ep.get('still_path')}" if ep.get("still_path") else "",
                    "vote_average": ep.get("vote_average", 0),
                    "vote_count": ep.get("vote_count", 0),
                }
            )
            
            # Create streaming sources
            create_video_sources(
                content_type="episode",
                content_id=episode.id
            )

    return series


def create_video_sources(
    content_type,
    content_id
):

    qualities = [
        "360p",
        "480p",
        "720p",
        "1080p"
    ]

    for quality in qualities:

        video, created = VideoSource.objects.get_or_create(
            content_type=content_type,
            content_id=content_id,
            quality=quality,

            defaults={

                # Example URLs
                "url":
                    f"https://cdn.streamix.com/"
                    f"{content_type}/"
                    f"{content_id}/"
                    f"{quality}.mp4",

                "is_hls": True,

                "master_playlist_url":
                    f"https://cdn.streamix.com/"
                    f"hls/{content_type}/"
                    f"{content_id}/master.m3u8",

                "file_size_mb":
                    1500,

                "duration_seconds":
                    7200,

                "is_active": True,

                "is_available": True,
            }
        )

        create_hls_stream(video)


def create_hls_stream(video_source):

    HLSStream.objects.get_or_create(
        video_source=video_source,

        defaults={

            "master_playlist_url":
                video_source.master_playlist_url,

            "variants": {

                "360p":
                    f"https://cdn.streamix.com/hls/"
                    f"{video_source.content_type}/"
                    f"{video_source.content_id}/360p.m3u8",

                "480p":
                    f"https://cdn.streamix.com/hls/"
                    f"{video_source.content_type}/"
                    f"{video_source.content_id}/480p.m3u8",

                "720p":
                    f"https://cdn.streamix.com/hls/"
                    f"{video_source.content_type}/"
                    f"{video_source.content_id}/720p.m3u8",

                "1080p":
                    f"https://cdn.streamix.com/hls/"
                    f"{video_source.content_type}/"
                    f"{video_source.content_id}/1080p.m3u8",
            },

            "bandwidth_info": {
                "360p": 800000,
                "480p": 1200000,
                "720p": 2500000,
                "1080p": 5000000,
            }
        }
    )

# ---------------------------
# BATCH SYNC HELPERS
# ---------------------------
def sync_popular_movies():
    data = client.get_popular_movies()

    for movie in data.get("results", []):
        sync_movie(movie["id"])


def sync_popular_tv():
    data = client.get_popular_tv()

    for tv in data.get("results", []):
        sync_tv_series(tv["id"])