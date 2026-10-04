from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import FarmCategory, FarmUpdate


def update_list(request):
    updates = FarmUpdate.objects.filter(is_published=True).select_related("category")
    category_slug = request.GET.get("category")
    if category_slug:
        updates = updates.filter(category__slug=category_slug)
    paginator = Paginator(updates, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "farms_hub/list.html", {
        "page_obj": page_obj,
        "categories": FarmCategory.objects.filter(published=True),
        "active_category": category_slug or "",
    })


def update_detail(request, slug):
    update = get_object_or_404(FarmUpdate.objects.select_related("category").prefetch_related("photos"), slug=slug, is_published=True)
    return render(request, "farms_hub/detail.html", {"update": update})
