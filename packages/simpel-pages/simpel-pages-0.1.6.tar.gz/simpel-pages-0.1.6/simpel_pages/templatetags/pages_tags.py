from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url

register = template.Library()


@register.simple_tag(takes_context=True)
def pageurl(context, page, fallback=None):
    request = context["request"]
    site = get_current_site(request)
    if page is None and fallback:
        return resolve_url(fallback)
    if not hasattr(page, "page_url"):
        raise ValueError("pageurl tag expected a Page object, got %r" % page)
    return page.page_url(site, request=context.get("request"))


@register.simple_tag(takes_context=True)
def routablepageurl(context, page, url_name, *args, **kwargs):
    # request = context["request"]
    # site = get_current_site(request)
    base_url = page.get_absolute_url()
    routed_url = page.reverse_subpage(url_name, args=args, kwargs=kwargs)
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url + routed_url


@register.filter(name="proper_paginate")
def proper_paginate(paginator, current_page, neighbors=3):
    if paginator.num_pages > 2 * neighbors:
        start_index = max(1, current_page - neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        if end_index < start_index + 2 * neighbors:
            end_index = start_index + 2 * neighbors
        elif start_index > end_index - 2 * neighbors:
            start_index = end_index - 2 * neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator.num_pages:
            start_index -= end_index - paginator.num_pages
            end_index = paginator.num_pages
        page_list = [f for f in range(start_index, end_index + 1)]
        return page_list[: (2 * neighbors + 1)]
    return paginator.page_range


@register.simple_tag(takes_context=True)
def replace_param(context, **kwargs):
    """ """
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
