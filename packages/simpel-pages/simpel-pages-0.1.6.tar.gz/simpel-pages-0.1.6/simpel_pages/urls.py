from django.urls import re_path

from . import views
from .settings import pages_settings

if pages_settings.APPEND_SLASH:
    # If APPEND_SLASH is True (the default value), we match a
    # (possibly empty) list of path segments ending in slashes.
    # CommonMiddleware will redirect requests without a trailing slash to
    # a URL with a trailing slash
    serve_pattern = r"^((?:[\w\-]+/)*)$"
else:
    # If WAGTAIL_APPEND_SLASH is False, allow Wagtail to serve pages on URLs
    # with and without trailing slashes
    serve_pattern = r"^([\w\-/]*)$"

urlpatterns = [
    re_path(r"^tag/$", views.serve_tags, name="serve_tag"),
    re_path(r"^tag/(?P<slug>[-\w]+)/$", views.serve_tag, name="serve_tag"),
    re_path(r"^category/$", views.serve_categories, name="serve_category"),
    re_path(r"^category/(?P<slug>[-\w]+)/$", views.serve_category, name="serve_category"),
    re_path(serve_pattern, views.serve_page, name="serve_pages"),
]
