from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import FarmUpdate


def update_list(request):
    updates = FarmUpdate.objects.filter(is_published=True)
    category = request.GET.get("category")
    if category:
        updates = updates.filter(category=category)
    paginator = Paginator(updates, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "farms_hub/list.html", {
        "page_obj": page_obj,
        "categories": FarmUpdate.CATEGORY_CHOICES,
        "active_category": category or "",
    })


def update_detail(request, slug):
    update = get_object_or_404(FarmUpdate, slug=slug, is_published=True)
    return render(request, "farms_hub/detail.html", {"update": update})
