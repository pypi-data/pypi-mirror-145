from django.apps import apps as django_apps
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured


class SimpelPageSitemap(Sitemap):
    def items(self):
        if not django_apps.is_installed("django.contrib.sites"):
            raise ImproperlyConfigured("SimpelPageSitemap requires django.contrib.sites, which isn't installed.")
        Site = django_apps.get_model("sites.Site")
        current_site = Site.objects.get_current()
        return current_site.simpelpages.filter(registration_required=False, live=True)
