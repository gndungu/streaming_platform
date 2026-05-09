from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.content.views import (
    MovieViewSet,
    TVSeriesViewSet,
    TrendingMoviesAPIView,
)

router = DefaultRouter()

router.register('movies', MovieViewSet)
router.register('series', TVSeriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'movies/trending/',
        TrendingMoviesAPIView.as_view(),
        name='trending-movies'
    ),
]