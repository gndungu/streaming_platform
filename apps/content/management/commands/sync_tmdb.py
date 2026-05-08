from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.content.sync_services import (
    sync_movie,
    sync_tv_series,
    sync_popular_movies,
    sync_popular_tv,
)


class Command(BaseCommand):

    help = "Sync content from TMDb"

    def add_arguments(self, parser):

        parser.add_argument(
            '--movie',
            type=int,
            help='Sync single movie by TMDb ID'
        )

        parser.add_argument(
            '--tv',
            type=int,
            help='Sync single TV series by TMDb ID'
        )

        parser.add_argument(
            '--popular-movies',
            action='store_true',
            help='Sync popular movies'
        )

        parser.add_argument(
            '--popular-tv',
            action='store_true',
            help='Sync popular TV series'
        )

    def handle(self, *args, **options):

        started_at = timezone.now()

        self.stdout.write(
            self.style.SUCCESS(
                f"TMDb sync started at {started_at}"
            )
        )

        try:

            # -------------------
            # Single Movie
            # -------------------
            if options.get('movie'):

                movie = sync_movie(
                    options['movie']
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Movie synced: {movie.title}"
                    )
                )

            # -------------------
            # Single TV Series
            # -------------------
            elif options.get('tv'):

                series = sync_tv_series(
                    options['tv']
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"TV series synced: {series.name}"
                    )
                )

            # -------------------
            # Popular Movies
            # -------------------
            elif options.get('popular_movies'):

                sync_popular_movies()

                self.stdout.write(
                    self.style.SUCCESS(
                        "Popular movies synced successfully"
                    )
                )

            # -------------------
            # Popular TV
            # -------------------
            elif options.get('popular_tv'):

                sync_popular_tv()

                self.stdout.write(
                    self.style.SUCCESS(
                        "Popular TV series synced successfully"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        "No sync option provided"
                    )
                )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"Sync failed: {str(e)}"
                )
            )

        finished_at = timezone.now()

        self.stdout.write(
            self.style.SUCCESS(
                f"TMDb sync completed at {finished_at}"
            )
        )