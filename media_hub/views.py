from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import MediaPost


def post_list(request):
    posts = MediaPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "media_hub/list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(MediaPost, slug=slug, is_published=True)
    return render(request, "media_hub/detail.html", {"post": post})
