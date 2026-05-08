from django.db import models


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    
    content_type = models.CharField(max_length=20)  # movie, episode
    content_id = models.PositiveIntegerField()
    
    # For movies: content_id is Movie.id
    # For episodes: content_id is Episode.id, with series/season tracking
    series_id = models.PositiveIntegerField(null=True, blank=True)
    season_number = models.IntegerField(null=True, blank=True)
    
    # Playback position
    last_position_seconds = models.IntegerField(default=0)  # where user left off
    duration_seconds = models.IntegerField(default=0)
    percent_completed = models.FloatField(default=0)
    
    # Quality watched
    quality = models.CharField(max_length=10, blank=True)
    
    # Watched status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    first_watched_at = models.DateTimeField(auto_now_add=True)
    last_watched_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'content_type', 'content_id']
        ordering = ['-last_watched_at']
    
    def save(self, *args, **kwargs):
        self.percent_completed = (self.last_position_seconds / self.duration_seconds * 100) if self.duration_seconds else 0
        if self.percent_completed >= 90 and not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)


class ContinueWatching(models.Model):
    """Derived from WatchHistory, for quick access"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='continue_watching')
    watch_history = models.OneToOneField(WatchHistory, on_delete=models.CASCADE)
    
    # Denormalized for performance
    content_type = models.CharField(max_length=20)
    content_id = models.PositiveIntegerField()
    title = models.CharField(max_length=500)
    poster_url = models.URLField(max_length=500, blank=True)
    last_position_seconds = models.IntegerField()
    
    updated_at = models.DateTimeField(auto_now=True)


class StreamHeartbeat(models.Model):
    """Track active streams for monitoring"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    
    content_type = models.CharField(max_length=20)
    content_id = models.PositiveIntegerField()
    quality = models.CharField(max_length=10)
    
    # Metrics
    bandwidth_mbps = models.FloatField(null=True, blank=True)
    buffer_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    
    last_heartbeat = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)



class HLSStream(models.Model):
    video_source = models.OneToOneField(VideoSource, on_delete=models.CASCADE)
    
    master_playlist_url = models.URLField(max_length=1000)
    
    # Variants
    variants = models.JSONField(default=dict)
    # Example:
    # {
    #   "144p": "https://cdn.example.com/streams/123/144p.m3u8",
    #   "360p": "https://cdn.example.com/streams/123/360p.m3u8",
    #   "720p": "https://cdn.example.com/streams/123/720p.m3u8",
    #   "1080p": "https://cdn.example.com/streams/123/1080p.m3u8"
    # }
    
    bandwidth_info = models.JSONField(default=dict)
    # Example:
    # {
    #   "144p": 200000,  # bits per second
    #   "360p": 800000,
    #   "720p": 2500000,
    #   "1080p": 5000000
    # }


