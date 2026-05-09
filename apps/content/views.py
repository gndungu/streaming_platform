from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, TVSeries
from .serializers import (
    MovieSerializer,
    TVSeriesSerializer,
    TrendingMovieSerializer 
)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    @action(detail=False)
    def trending(self, request):

        queryset = self.queryset.order_by('-popularity')[:20]

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False)
    def featured(self, request):

        queryset = self.queryset.filter(is_featured=True)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class TVSeriesViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TVSeries.objects.filter(is_active=True)
    serializer_class = TVSeriesSerializer
    permission_classes = [AllowAny]

    @action(detail=False)
    def trending(self, request):

        queryset = self.queryset.order_by('-popularity')[:20]

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class TrendingMoviesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        movies = (
            Movie.objects
            .filter(is_active=True)
            .order_by('-popularity')[:20]
        )

        serializer = TrendingMovieSerializer(
            movies,
            many=True
        )

        return Response(serializer.data)


# ViewSet Example
# class MovieViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Movie.objects.filter(is_active=True)
#     serializer_class = MovieSerializer
#     pagination_class = CustomPagination
    
#     @action(detail=False, methods=['get'])
#     def trending(self, request):
#         trending = self.get_queryset().order_by('-popularity')[:20]
#         serializer = self.get_serializer(trending, many=True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['post'])
#     def add_to_watchlist(self, request, pk=None):
#         movie = self.get_object()
#         watchlist, created = Watchlist.objects.get_or_create(
#             user=request.user, movie=movie
#         )
#         return Response({'status': 'added'})


# # Standard response wrapper
# def api_response(data=None, message=None, success=True, status=200):
#     return Response({
#         'success': success,
#         'message': message,
#         'data': data,
#         'timestamp': timezone.now().isoformat()
#     }, status=status)

# # Paginated response
# {
#     "success": true,
#     "data": {
#         "count": 1250,
#         "next": "https://api.example.com/v1/movies/?page=2",
#         "previous": null,
#         "results": [...]
#     },
#     "message": "Movies retrieved successfully"
# }
