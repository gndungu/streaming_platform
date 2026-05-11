from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)

from rest_framework.permissions import (
    IsAuthenticated
)

from django.shortcuts import get_object_or_404

from apps.content.models import (
    Movie,
    Episode,
    VideoSource
)

from apps.streaming.models import (
    WatchHistory,
    ContinueWatching,
    StreamHeartbeat
)

from .serializers import (
    MovieStreamSerializer,
    EpisodeStreamSerializer,
    WatchHistorySerializer,
    ContinueWatchingSerializer,
    StreamHeartbeatSerializer
)


# =====================================
# WATCH MOVIE
# =====================================

class WatchMovieAPIView(
    RetrieveAPIView
):

    # permission_classes = [IsAuthenticated]

    queryset = Movie.objects.filter(
        is_active=True
    )

    serializer_class = MovieStreamSerializer


# =====================================
# WATCH EPISODE
# =====================================

class WatchEpisodeAPIView(
    RetrieveAPIView
):

    permission_classes = [IsAuthenticated]

    queryset = Episode.objects.all()

    serializer_class = EpisodeStreamSerializer


# =====================================
# SAVE WATCH PROGRESS
# =====================================

class SaveWatchProgressAPIView(
    APIView
):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data

        history, created = (
            WatchHistory.objects.update_or_create(
                user=request.user,
                content_type=data["content_type"],
                content_id=data["content_id"],

                defaults={
                    "series_id":
                        data.get("series_id"),

                    "season_number":
                        data.get("season_number"),

                    "last_position_seconds":
                        data.get(
                            "last_position_seconds",
                            0
                        ),

                    "duration_seconds":
                        data.get(
                            "duration_seconds",
                            0
                        ),

                    "quality":
                        data.get("quality", "")
                }
            )
        )

        # =====================================
        # Continue Watching
        # =====================================

        if data["content_type"] == "movie":

            movie = Movie.objects.get(
                    id=data["content_id"]
                )

            title = movie.title

            poster = movie.poster_path

        else:

            episode = Episode.objects.get(
                    id=data["content_id"]
                )

            title = episode.name

            poster = episode.still_path

        ContinueWatching.objects.update_or_create(
            user=request.user,
            watch_history=history,

            defaults={
                "content_type":
                    history.content_type,

                "content_id":
                    history.content_id,

                "title": title,

                "poster_url":
                    poster,

                "last_position_seconds":
                    history.last_position_seconds
            }
        )

        serializer = WatchHistorySerializer(history)

        return Response(serializer.data)


# =====================================
# CONTINUE WATCHING
# =====================================

class ContinueWatchingAPIView(
    ListAPIView
):

    permission_classes = [IsAuthenticated]

    serializer_class = ContinueWatchingSerializer

    def get_queryset(self):

        return (
            ContinueWatching.objects.filter(
                user=self.request.user
            )
        )


# =====================================
# WATCH HISTORY
# =====================================

class WatchHistoryAPIView(
    ListAPIView
):

    permission_classes = [IsAuthenticated]

    serializer_class = WatchHistorySerializer

    def get_queryset(self):

        return (
            WatchHistory.objects.filter(
                user=self.request.user
            )
        )


# =====================================
# STREAM HEARTBEAT
# =====================================

class StreamHeartbeatAPIView(
    APIView
):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = StreamHeartbeatSerializer(
                data=request.data
            )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            user=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
