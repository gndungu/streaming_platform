
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    cast = CastSerializer(many=True, read_only=True, source='cast_set')
    crew = CrewSerializer(many=True, read_only=True, source='crew_set')
    videos = VideoSerializer(many=True, read_only=True, source='video_set')
    is_in_watchlist = serializers.SerializerMethodField()
    watch_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'original_title', 'overview', 'tagline',
            'release_date', 'runtime', 'vote_average', 'vote_count', 'popularity',
            'age_rating', 'poster_path', 'backdrop_path', 'genres', 'cast', 'crew',
            'videos', 'is_in_watchlist', 'watch_progress'
        ]
    
    def get_is_in_watchlist(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Watchlist.objects.filter(user=user, movie=obj).exists()
        return False
    
    def get_watch_progress(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            history = WatchHistory.objects.filter(
                user=user, content_type='movie', content_id=obj.id
            ).first()
            if history:
                return {
                    'last_position': history.last_position_seconds,
                    'percent_completed': history.percent_completed
                }
        return None


