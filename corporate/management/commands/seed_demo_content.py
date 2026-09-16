from django.core.management.base import BaseCommand
from django.utils import timezone

from corporate.models import FAQItem
from farms_hub.models import FarmUpdate
from media_hub.models import MediaPost


class Command(BaseCommand):
    help = "Seeds placeholder Media/Farms/FAQ content so the hubs aren't empty in local dev. Not real copy — replace in Phase 4."

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

        faq_seed = [
            ("What does AfraViva do?", "AfraViva runs media, farms and community initiatives. Homes is managed separately at homes.afraviva.com."),
            ("How can I get in touch?", "Use the contact form on this site or email kiokoitdev@afraviva.com."),
        ]
        for i, (q, a) in enumerate(faq_seed):
            FAQItem.objects.get_or_create(question=q, defaults={"answer": a, "order": i})

        self.stdout.write(self.style.SUCCESS("Seeded placeholder demo content."))
