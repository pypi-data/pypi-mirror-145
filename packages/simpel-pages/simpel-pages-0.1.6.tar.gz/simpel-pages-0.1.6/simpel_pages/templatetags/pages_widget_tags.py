from django import template
from django.template import loader

from ..models import Category, Page, Tag

register = template.Library()


@register.simple_tag(takes_context=True)
def popular_pages(context, title, obj=None, number=5, template_name=None):
    if obj is not None:
        qs = obj.childs.all()
    else:
        qs = Page.objects.all()
    qs = qs.filter(index=False).live().order_by("-visitor_count")[:number]
    context = {"title": title, "pages": qs}
    if template_name is None:
        template_name = "simpel_pages/widgets/page_list.html"
    template = loader.get_template(template_name)
    return template.render(context)


@register.simple_tag(takes_context=True)
def recent_pages(context, title, obj=None, number=5, template_name=None):
    if obj is not None:
        qs = obj.childs.all()
    else:
        qs = Page.objects.all()
    qs = qs.filter(index=False).live().order_by("-created_at")[:number]
    context = {"title": title, "pages": qs}
    if template_name is None:
        template_name = "simpel_pages/widgets/page_list.html"
    template = loader.get_template(template_name)
    return template.render(context)


@register.simple_tag(takes_context=True)
def related_pages_by_category(context, title, obj, number=5, template_name=None):
    qs = obj.get_related_by_category(number)
    context = {"title": title, "pages": qs}
    if template_name is None:
        template_name = "simpel_pages/widgets/page_list.html"
    template = loader.get_template(template_name)
    return template.render(context)


@register.simple_tag(takes_context=True)
def related_pages_by_tags(context, title, obj, number=5, template_name=None):
    qs = obj.get_related_by_tags(number)
    context = {"title": title, "pages": qs}
    if template_name is None:
        template_name = "simpel_pages/widgets/page_list.html"
    template = loader.get_template(template_name)
    return template.render(context)


@register.simple_tag(takes_context=True)
def related_pages(context, title, obj, number=5, by=None, template_name=None):
    if by == "tags":
        return related_pages_by_tags(context, title, obj, number, template_name)
    else:
        return related_pages_by_category(context, title, obj, number, template_name)


@register.simple_tag(takes_context=True)
def category_list(context, title, number=5, template_name=None):
    qs = Category.objects.all()
    context = {"title": title, "categories": qs[:number]}
    if template_name is None:
        template_name = "simpel_pages/widgets/category_list.html"
    template = loader.get_template(template_name)
    return template.render(context)


@register.simple_tag(takes_context=True)
def tags_list(context, title, number=5, template_name=None):
    qs = Tag.objects.popular()
    context = {"title": title, "tags": qs[:number]}
    if template_name is None:
        template_name = "simpel_pages/widgets/tags_list.html"
    template = loader.get_template(template_name)
    return template.render(context)
