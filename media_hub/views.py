from django.core.paginator import Paginator
from csp.decorators import csp_update
from django.shortcuts import get_object_or_404, render

from .models import MediaPost


# The list page embeds TikTok's creator profile (media_hub/_tiktok_follow.html):
# www.tiktok.com/embed.js redirects to the real script on TikTok's
# ttwstatic.com CDN, which then renders the profile in a www.tiktok.com iframe.
@csp_update({
    "script-src": ["https://www.tiktok.com", "https://*.ttwstatic.com"],
    "frame-src": ["https://www.tiktok.com"],
})
def post_list(request):
    posts = MediaPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "media_hub/list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(MediaPost, slug=slug, is_published=True)
    return render(request, "media_hub/detail.html", {"post": post})
