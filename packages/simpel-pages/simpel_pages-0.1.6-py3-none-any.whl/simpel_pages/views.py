from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView

from simpel_hookup import core as hookup

from simpel_pages.models import Category, Tag
from simpel_pages.settings import pages_settings

from .helpers import log_visitor


@csrf_protect
def serve_page(request, path):
    # we need a valid Site object corresponding to this request in order to proceed
    site = get_current_site(request)
    if not site:
        raise Http404

    path_components = [component for component in path.split("/") if component]
    page, args, kwargs = site.rootpage.page.specific.route(request, path_components)

    for fn in hookup.get_hooks("PAGES_BEFORE_SERVE"):
        result = fn(page, request, args, kwargs)
        if isinstance(result, HttpResponse):
            return result
    log_visitor(request, content=page)
    if request.user.is_authenticated:
        page.readers.add(request.user)
    return page.serve(request, *args, **kwargs)


@csrf_protect
def serve_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    site = get_current_site(request)
    real_model = request.GET.get("type", None)
    filters = dict()
    if real_model is not None:
        filters["real_model"] = real_model
    filters["category__slug__in"] = [category.slug]
    queryset = site.rootpage.page.get_descendants().filter(**filters).live()
    log_visitor(request, content=category)
    return ListView.as_view(
        queryset=queryset,
        paginate_by=pages_settings.ITEM_PER_PAGE,
        template_name="simpel_pages/category.html",
        extra_context={"object": category},
    )(request)


@csrf_protect
def serve_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    site = get_current_site(request)
    real_model = request.GET.get("type", None)
    filters = dict()
    if real_model is not None:
        filters["real_model"] = real_model
    filters["tags__slug__in"] = [tag.slug]
    queryset = site.rootpage.page.get_descendants().filter(**filters).live()
    log_visitor(request, content=tag)
    return ListView.as_view(
        queryset=queryset,
        paginate_by=pages_settings.ITEM_PER_PAGE,
        template_name="simpel_pages/tag.html",
        extra_context={"object": tag},
    )(request)


def serve_tags(request):
    return ListView.as_view(
        queryset=Tag.objects.all(),
        paginate_by=pages_settings.CATEGORY_PER_PAGE,
        template_name="simpel_pages/tag_list.html",
    )(request)


def serve_categories(request):
    return ListView.as_view(
        queryset=Category.objects.all(),
        paginate_by=pages_settings.TAG_PER_PAGE,
        template_name="simpel_pages/category_list.html",
    )(request)
