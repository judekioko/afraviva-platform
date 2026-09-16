from django.core.management.base import BaseCommand
from django.utils import timezone

from farms_hub.models import FarmUpdate
from media_hub.models import MediaPost


class Command(BaseCommand):
    help = "Seeds placeholder Media/Farms content so the hubs aren't empty in local dev. Not real copy — replace in Phase 4. (FAQ content is real, loaded via migration.)"

    def handle(self, *args, **options):
        now = timezone.now()

        media_seed = [
            ("AfraViva Media launches community reporting desk", "Placeholder body text for a Media post."),
            ("Behind the scenes: covering local stories", "Placeholder body text for a Media post."),
            ("Q&A with the AfraViva Media team", "Placeholder body text for a Media post."),
        ]
        for title, body in media_seed:
            MediaPost.objects.get_or_create(
                title=title, defaults={"body": body, "is_published": True, "published_at": now}
            )

        farm_seed = [
            ("Rains bring a strong maize season", "crop", "Placeholder body text for a Farm update."),
            ("New water point completed for the livestock program", "infrastructure", "Placeholder body text for a Farm update."),
            ("Community farmers group welcomes new members", "community", "Placeholder body text for a Farm update."),
        ]
        for title, category, body in farm_seed:
            FarmUpdate.objects.get_or_create(
                title=title, defaults={"body": body, "category": category, "is_published": True, "published_at": now}
            )

        self.stdout.write(self.style.SUCCESS("Seeded placeholder demo content."))
