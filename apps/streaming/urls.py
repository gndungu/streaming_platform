from django.urls import path

from apps.streaming.views import (

    WatchMovieAPIView,
    WatchEpisodeAPIView,

    SaveWatchProgressAPIView,

    ContinueWatchingAPIView,

    WatchHistoryAPIView,

    StreamHeartbeatAPIView
)

urlpatterns = [

    # =====================================
    # STREAMING
    # =====================================

    path(
        "movies/<int:pk>/",
        WatchMovieAPIView.as_view()
    ),

    path(
        "episodes/<int:pk>/",
        WatchEpisodeAPIView.as_view()
    ),

    # =====================================
    # WATCH PROGRESS
    # =====================================

    path(
        "progress/save/",
        SaveWatchProgressAPIView.as_view()
    ),

    path(
        "continue-watching/",
        ContinueWatchingAPIView.as_view()
    ),

    path(
        "history/",
        WatchHistoryAPIView.as_view()
    ),

    # =====================================
    # HEARTBEAT
    # =====================================

    path(
        "heartbeat/",
        StreamHeartbeatAPIView.as_view()
    ),
]