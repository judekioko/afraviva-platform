from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "No-op: Media, Farms and FAQ launch content are now loaded via data "
        "migrations (media_hub/0002, farms_hub/0002, corporate/0002), which "
        "run automatically on `migrate`. Kept as a stable entry point in case "
        "future dev-only seed data is needed."
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Nothing to seed — content is loaded via migrations."))
