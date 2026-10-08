from django.core.paginator import Paginator
from csp.decorators import csp_update
from django.shortcuts import get_object_or_404, render

from .models import FeaturedTikTok, MediaPost


# The list page plays featured TikToks in TikTok's single-video player iframe
# (media_hub/_tiktok_follow.html). No TikTok script runs on our page.
@csp_update({"frame-src": ["https://www.tiktok.com"]})
def post_list(request):
    posts = MediaPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "media_hub/list.html", {
        "page_obj": page_obj,
        "tiktoks": FeaturedTikTok.objects.filter(published=True)[:3],
    })


def post_detail(request, slug):
    post = get_object_or_404(MediaPost, slug=slug, is_published=True)
    return render(request, "media_hub/detail.html", {"post": post})
