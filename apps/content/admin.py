from django.contrib import admin
from apps.content.models import (
    ContentType,
    Movie,
    TVSeries,
    Season,
    Episode,
    Genre,
    Keyword,
    Language,
    Country,
    ProductionCompany,
    Network,
    Person,
    Cast,
    Crew,
    VideoSource,
    CachedImage,
    ContentApproval,
    ContentSchedule,
    ContentFlag,
)


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'release_date',
        'vote_average',
        'is_active',
        'is_featured',
    ]

    list_filter = [
        'is_active',
        'is_featured',
        'status',
        'release_date',
    ]

    search_fields = [
        'title',
        'original_title',
        'overview',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'last_tmdb_sync',
    ]

    filter_horizontal = [
        'genres',
        'keywords',
        'production_companies',
        'production_countries',
        'languages',
    ]


@admin.register(TVSeries)
class TVSeriesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'first_air_date',
        'number_of_seasons',
        'vote_average',
        'is_active',
    ]

    list_filter = [
        'status',
        'is_active',
        'is_featured',
    ]

    search_fields = [
        'name',
        'original_name',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'last_tmdb_sync',
    ]

    filter_horizontal = [
        'genres',
        'keywords',
        'networks',
    ]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'series',
        'season_number',
        'episode_count',
    ]

    list_filter = ['series']
    search_fields = ['name', 'series__name']


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'season',
        'episode_number',
        'name',
        'air_date',
    ]

    list_filter = ['season']
    search_fields = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    search_fields = ['name']


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    search_fields = ['name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['iso_639_1', 'name']
    search_fields = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['iso_3166_1', 'name']
    search_fields = ['name']


@admin.register(ProductionCompany)
class ProductionCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'origin_country']
    search_fields = ['name']


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'origin_country']
    search_fields = ['name']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'birthday',
        'popularity',
    ]

    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'person',
        'movie',
        'series',
        'character',
        'order',
    ]

    search_fields = [
        'person__name',
        'character',
    ]


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'person',
        'movie',
        'series',
        'job',
        'department',
    ]

    search_fields = [
        'person__name',
        'job',
        'department',
    ]


@admin.register(VideoSource)
class VideoSourceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content_type',
        'content_id',
        'quality',
        'is_active',
        'is_available',
    ]

    list_filter = [
        'content_type',
        'quality',
        'is_active',
        'is_available',
    ]

    search_fields = [
        'url',
        'storage_path',
    ]


@admin.register(CachedImage)
class CachedImageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'image_type',
        'width',
        'height',
        'last_accessed',
    ]

    search_fields = [
        'tmdb_path',
        'local_url',
    ]


@admin.register(ContentApproval)
class ContentApprovalAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content_type',
        'content_id',
        'status',
        'submitted_by',
        'reviewed_by',
        'created_at',
    ]

    list_filter = [
        'status',
        'auto_approved',
    ]

    search_fields = [
        'review_notes',
    ]


@admin.register(ContentSchedule)
class ContentScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content_type',
        'content_id',
        'release_date',
        'is_visible_before_release',
    ]

    list_filter = [
        'content_type',
        'is_visible_before_release',
    ]


@admin.register(ContentFlag)
class ContentFlagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content_type',
        'content_id',
        'reason',
        'status',
        'reported_by',
        'created_at',
    ]

    list_filter = [
        'reason',
        'status',
    ]

    search_fields = [
        'description',
    ]
