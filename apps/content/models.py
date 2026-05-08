from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ContentType(models.Model):
    """Enum-like table: movie, tv_series, episode"""
    name = models.CharField(max_length=50, unique=True)


class Movie(models.Model):
    # TMDb identifiers
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    
    # Basic info
    title = models.CharField(max_length=500, db_index=True)
    original_title = models.CharField(max_length=500, blank=True)
    tagline = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    
    # Dates & runtime
    release_date = models.DateField(null=True, blank=True, db_index=True)
    runtime = models.IntegerField(null=True, blank=True)  # minutes
    
    # Financial (optional, from TMDb)
    budget = models.BigIntegerField(null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    
    # Ratings
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0, db_index=True)
    
    # Age rating (certification)
    age_rating = models.CharField(max_length=10, blank=True)  # G, PG, PG-13, R, NC-17, etc.
    
    # Status
    status = models.CharField(max_length=50, default='released')  # released, rumored, planned, in_production, post_production, cancelled
    
    # Images - store URLs
    poster_path = models.URLField(max_length=500, blank=True)
    backdrop_path = models.URLField(max_length=500, blank=True)
    logo_path = models.URLField(max_length=500, blank=True)
    
    # Local overrides (admin can manually change)
    custom_title = models.CharField(max_length=500, blank=True)
    custom_overview = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_tmdb_sync = models.DateTimeField(null=True)
    
    # Relationships
    genres = models.ManyToManyField('Genre', related_name='movies')
    keywords = models.ManyToManyField('Keyword', related_name='movies')
    production_companies = models.ManyToManyField('ProductionCompany', related_name='movies')
    production_countries = models.ManyToManyField('Country', related_name='movies')
    languages = models.ManyToManyField('Language', related_name='movies')
    
    class Meta:
        indexes = [
            models.Index(fields=['-popularity']),
            models.Index(fields=['-release_date']),
            models.Index(fields=['-vote_average']),
        ]
    
    @property
    def display_title(self):
        return self.custom_title or self.title


class TVSeries(models.Model):
    # Similar to Movie but TV-specific
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=500, db_index=True)
    original_name = models.CharField(max_length=500, blank=True)
    overview = models.TextField(blank=True)
    
    # TV specific
    first_air_date = models.DateField(null=True, blank=True)
    last_air_date = models.DateField(null=True, blank=True)
    number_of_seasons = models.IntegerField(default=0)
    number_of_episodes = models.IntegerField(default=0)
    episode_run_time = models.IntegerField(null=True, blank=True)  # average minutes
    
    # Status: returning, ended, cancelled, in_production
    status = models.CharField(max_length=50, default='returning')
    
    # Networks (broadcasters)
    networks = models.ManyToManyField('Network', related_name='series')
    
    # Same rating/popularity/images fields as Movie
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0, db_index=True)
    poster_path = models.URLField(max_length=500, blank=True)
    backdrop_path = models.URLField(max_length=500, blank=True)
    
    # Local overrides
    custom_name = models.CharField(max_length=500, blank=True)
    custom_overview = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_tmdb_sync = models.DateTimeField(null=True)
    
    # Relationships
    genres = models.ManyToManyField('Genre', related_name='series')
    keywords = models.ManyToManyField('Keyword', related_name='series')
    
    @property
    def display_name(self):
        return self.custom_name or self.name


class Season(models.Model):
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='seasons')
    
    season_number = models.IntegerField(db_index=True)
    name = models.CharField(max_length=500, blank=True)
    overview = models.TextField(blank=True)
    
    air_date = models.DateField(null=True, blank=True)
    episode_count = models.IntegerField(default=0)
    
    poster_path = models.URLField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['series', 'season_number']
        ordering = ['season_number']


class Episode(models.Model):
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    
    episode_number = models.IntegerField(db_index=True)
    name = models.CharField(max_length=500)
    overview = models.TextField(blank=True)
    
    air_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)  # minutes
    
    still_path = models.URLField(max_length=500, blank=True)  # episode screenshot
    
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    
    # Video sources (streaming/download)
    video_sources = models.JSONField(default=list)  # [{quality, url, size_mb}]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['season', 'episode_number']
        ordering = ['episode_number']


# Metadata Models
class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    

class Keyword(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)


class Language(models.Model):
    iso_639_1 = models.CharField(max_length=2, unique=True)  # 'en'
    name = models.CharField(max_length=100)  # 'English'


class Country(models.Model):
    iso_3166_1 = models.CharField(max_length=2, unique=True)  # 'US'
    name = models.CharField(max_length=100)  # 'United States'


class ProductionCompany(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    logo_path = models.URLField(max_length=500, blank=True)
    origin_country = models.CharField(max_length=2, blank=True)


class Network(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    logo_path = models.URLField(max_length=500, blank=True)
    origin_country = models.CharField(max_length=2, blank=True)


# People Models
class Person(models.Model):
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    biography = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    profile_path = models.URLField(max_length=500, blank=True)
    popularity = models.FloatField(default=0)
    
    # External IDs
    imdb_id = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cast(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, null=True, blank=True)
    
    character = models.CharField(max_length=200)
    order = models.IntegerField(default=0)  # billing order
    cast_id = models.IntegerField()
    
    class Meta:
        unique_together = ['person', 'movie', 'series', 'character']
        ordering = ['order']


class Crew(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, null=True, blank=True)
    
    job = models.CharField(max_length=100)  # Director, Writer, Producer, etc.
    department = models.CharField(max_length=100)
    credit_id = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ['person', 'movie', 'series', 'job']


# Video Source Model (for external/internal video storage)
class VideoSource(models.Model):
    QUALITY_CHOICES = [
        ('144p', '144p'),
        ('240p', '240p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4k', '4K'),
    ]
    
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('episode', 'Episode'),
    ]
    
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content_id = models.PositiveIntegerField()  # ID of Movie or Episode
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)
    
    # Storage
    url = models.URLField(max_length=1000)  # Direct URL or CDN URL
    file_size_mb = models.FloatField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    # For internal storage (S3 path)
    storage_path = models.CharField(max_length=500, blank=True)
    
    # For HLS streaming
    is_hls = models.BooleanField(default=False)
    master_playlist_url = models.URLField(max_length=1000, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)  # Not expired/deleted
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['content_type', 'content_id', 'quality']


# Image Cache Model (optional, for CDN fallback)
class CachedImage(models.Model):
    tmdb_path = models.CharField(max_length=500, unique=True)  # Original TMDb path
    local_url = models.URLField(max_length=1000)  # Our CDN URL
    image_type = models.CharField(max_length=50)  # poster, backdrop, profile, still
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    last_accessed = models.DateTimeField(auto_now=True)
    

class ContentApproval(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_review', 'Needs Manual Review'),
    ]
    
    content_type = models.CharField(max_length=20)  # movie, series, episode
    content_id = models.PositiveIntegerField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # admin who submitted
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    
    review_notes = models.TextField(blank=True)
    auto_approved = models.BooleanField(default=False)  # Auto-approved from TMDb?
    
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['content_type', 'content_id']



class ContentSchedule(models.Model):
    content_type = models.CharField(max_length=20)  # movie, episode
    content_id = models.PositiveIntegerField()
    
    release_date = models.DateTimeField(db_index=True)
    is_visible_before_release = models.BooleanField(default=False)  # Show coming soon page?
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_available(self):
        return timezone.now() >= self.release_date


class ContentFlag(models.Model):
    REASON_CHOICES = [
        ('broken_link', 'Broken Video Link'),
        ('wrong_metadata', 'Wrong Title/Description'),
        ('wrong_episode', 'Wrong Episode'),
        ('poor_quality', 'Poor Video Quality'),
        ('copyright', 'Copyright Infringement'),
        ('other', 'Other'),
    ]
    
    content_type = models.CharField(max_length=20)
    content_id = models.PositiveIntegerField()
    
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField()
    
    status = models.CharField(max_length=20, default='pending')  # pending, resolved, dismissed
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_flags')
    resolution_note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)



