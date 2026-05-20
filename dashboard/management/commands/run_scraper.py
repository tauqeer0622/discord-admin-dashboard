from django.core.management.base import (
    BaseCommand
)

from scraper.api_scraper import (
    run_scraper
)


class Command(BaseCommand):

    help = (
        "Run Discord scraper"
    )

    def handle(self, *args, **kwargs):

        self.stdout.write(

            self.style.SUCCESS(
                "Starting scraper..."
            )
        )

        run_scraper()

        self.stdout.write(

            self.style.SUCCESS(
                "Scraper finished."
            )
        )