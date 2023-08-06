from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand

from simpel_themes.models import PathModelTemplate

from simpel_pages.models import Page, RootPage


class Command(BaseCommand):
    help = "Install demo pages"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        home_template, _ = PathModelTemplate.objects.get_or_create(
            template="simpel_pages/home.html",
            defaults={
                "name": "Page Home",
            },
        )
        index_template, _ = PathModelTemplate.objects.get_or_create(
            template="simpel_pages/index.html",
            defaults={
                "name": "Page Index",
            },
        )
        detail_template, _ = PathModelTemplate.objects.get_or_create(
            template="simpel_pages/detail.html",
            defaults={
                "name": "Page Detail",
            },
        )

        site = get_current_site(request=None)
        root_page = getattr(site, "rootpage", None)
        if root_page is None:
            root_page, _ = RootPage.objects.get_or_create(site=site)

        if root_page.page is None:
            home_page, _ = Page.objects.get_or_create(
                parent=None,
                slug="home",
                defaults={
                    "template": home_template,
                    "title": "Home Page",
                    "slug": "home",
                    "index": True,
                },
            )
            root_page.page = home_page
            root_page.save()
        else:
            home_page = root_page.page

        blog_page, _ = Page.objects.get_or_create(
            parent=home_page,
            slug="blog",
            defaults={
                "template": index_template,
                "title": "Blog",
                # "slug": "blog",
                "index": True,
            },
        )
        post_1, _ = Page.objects.get_or_create(
            parent=blog_page,
            slug="post-1",
            defaults={
                "template": detail_template,
                "title": "Post 1",
                # "slug": "post-1",
            },
        )
        post_2, _ = Page.objects.get_or_create(
            parent=blog_page,
            slug="post-2",
            defaults={
                "template": detail_template,
                "title": "Post 2",
                # "slug": "post-2",
            },
        )
        post_3, _ = Page.objects.get_or_create(
            parent=blog_page,
            slug="post-3",
            defaults={
                "template": detail_template,
                "title": "Post 3",
                # "slug": "post-3",
            },
        )
        toc_page, _ = Page.objects.get_or_create(
            parent=home_page,
            slug="term-of-condition",
            defaults={
                "index": True,
                "title": "Term of Condition",
                # "slug": "term-of-condition",
            },
        )
        privacy_page, _ = Page.objects.get_or_create(
            parent=home_page,
            slug="privacy-policy",
            defaults={
                "index": True,
                "title": "Privacy Policy",
                # "slug": "privacy-policy",
            },
        )
