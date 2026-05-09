from rest_framework import serializers

from apps.streaming.models import (
    WatchHistory,
    ContinueWatching,
    StreamHeartbeat,
    HLSStream
)

from apps.content.models import (
    Movie,
    Episode,
    VideoSource
)


class HLSStreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = HLSStream
        fields = [
            "master_playlist_url",
            "variants",
            "bandwidth_info"
        ]


class VideoSourceSerializer(serializers.ModelSerializer):

    hls_stream = HLSStreamSerializer(
        read_only=True
    )

    class Meta:
        model = VideoSource
        fields = [
            "id",
            "quality",
            "url",
            "is_hls",
            "duration_seconds",
            "file_size_mb",
            "master_playlist_url",
            "hls_stream"
        ]


class MovieStreamSerializer(
    serializers.ModelSerializer
):

    video_sources = serializers.SerializerMethodField()

    class Meta:
        model = Movie

        fields = [
            "id",
            "title",
            "overview",
            "poster_path",
            "backdrop_path",
            "runtime",
            "video_sources"
        ]

    def get_video_sources(self, obj):

        videos = VideoSource.objects.filter(
                content_type="movie",
                content_id=obj.id,
                is_active=True,
                is_available=True
            )

        return VideoSourceSerializer(
            videos,
            many=True
        ).data


class EpisodeStreamSerializer(
    serializers.ModelSerializer
):

    video_sources = serializers.SerializerMethodField()

    class Meta:
        model = Episode

        fields = [
            "id",
            "name",
            "overview",
            "still_path",
            "runtime",
            "video_sources"
        ]

    def get_video_sources(self, obj):

        videos = VideoSource.objects.filter(
                content_type="episode",
                content_id=obj.id,
                is_active=True,
                is_available=True
            )

        return VideoSourceSerializer(
            videos,
            many=True
        ).data


class WatchHistorySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = WatchHistory
        fields = "__all__"
        read_only_fields = [
            "percent_completed",
            "completed_at",
            "first_watched_at",
            "last_watched_at"
        ]


class ContinueWatchingSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ContinueWatching
        fields = "__all__"


class StreamHeartbeatSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = StreamHeartbeat
        fields = "__all__"